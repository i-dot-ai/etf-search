import enum
import functools
import inspect
import types

import marshmallow
from django.contrib.auth.decorators import login_required
from django.http import Http404

from eva_reg.settings import ALLOWED_CIVIL_SERVICE_DOMAINS

from . import choices, models

event_names = set()

SEPARATOR = "|"


def dictify(*args, **kwargs):
    if (len(args) == 1) and callable(args[0]):
        func = args[0]

        @functools.wraps(func)
        def _inner(*args, **kwargs):
            return dict(func(*args, **kwargs))

        return _inner
    else:
        d = {}
        for arg in args:
            d.update(arg)
        d.update(kwargs)
        return d


class DuplicateEvent(Exception):
    pass


def get_arguments(func, *args, **kwargs):
    """Calculate what the args would be inside a function"""
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    arguments = bound_args.arguments
    return arguments


def _register_event(event_name, arguments):
    event_names.add(event_name)
    arguments = {key: value for (key, value) in arguments.items() if key != "self"}
    event = models.Event(name=event_name, data=arguments)
    event.save()


def resolve_schema(schema):
    """Allow either a class or an instance to be passed"""
    if isinstance(schema, marshmallow.schema.SchemaMeta):
        schema = schema()
    return schema


def register_event(event_name):
    def _decorator(func):
        func.event_name = event_name

        @functools.wraps(func)
        def _inner(*args, **kwargs):
            arguments = get_arguments(func, *args, **kwargs)
            _register_event(event_name, arguments)
            return func(*args, **kwargs)

        return _inner

    return _decorator


def process_self(func, arguments):
    """Remove `self` from arguments and bind it to func"""
    if "self" in arguments:
        func = functools.partial(func, arguments["self"])
        arguments = {k: v for k, v in arguments.items() if k != "self"}
    return func, arguments


def check_edit_evaluation_permission(func):
    def wrapper(request, *args, **kwargs):
        evaluation_id = kwargs["evaluation_id"]
        evaluation = models.Evaluation.objects.get(pk=evaluation_id)
        evaluation_users = evaluation.users.all()
        if request.user not in evaluation_users:
            raise Http404("Evaluation not found")
        return func(request, *args, **kwargs)

    return wrapper


def apply_schema(schema, data, load_or_dump):
    """Apply a schema to some data"""
    if not schema:
        return data
    if load_or_dump not in ("load", "dump"):
        raise ValueError(f"Unknown value {load_or_dump}")
    if schema:
        schema = resolve_schema(schema)
        arguments = getattr(schema, load_or_dump)(data)
    return arguments


def with_schema(default=None, load=None, dump=None):
    """Applies the load_schema.load on the arguments to the function,
    and dump_schema.dump on the result of the function.

    This ensures that validation has been passed and that the result of the
    function is JSON serialisable"""
    load_schema = load or default
    dump_schema = dump or default

    def _decorator(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            arguments = get_arguments(func, *args, **kwargs)
            bound_func, arguments = process_self(func, arguments)
            arguments = apply_schema(load_schema, arguments, "load")
            result = bound_func(**arguments)
            result = apply_schema(dump_schema, result, "dump")
            return result

        return _inner

    return _decorator


class Facade:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        all_event_names = tuple(
            event_name for entity in kwargs.values() for event_name in getattr(entity, "event_names", ())
        )
        if len(all_event_names) != len(set(all_event_names)):
            raise DuplicateEvent(all_event_names)
        self.event_names = all_event_names


class Entity:
    def __init__(self):
        possible_methods = (getattr(self, key) for key in dir(self) if not key.startswith("_"))
        possible_event_names = (getattr(item, "event_name", None) for item in possible_methods)
        self.event_names = tuple(item for item in possible_event_names if item)


class ChoicesMeta(enum.EnumMeta):
    """A metaclass for creating a enum choices."""

    def __new__(metacls, classname, bases, classdict, **kwds):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if isinstance(value, (list, tuple)) and len(value) > 1 and isinstance(value[-1], str):
                value, label = value
            elif hasattr(value, "name"):
                label = str(value.name)
            else:
                label = value
                value = key
            labels.append(label)
            # Use dict.__setitem__() to suppress defenses against double
            # assignment in enum's classdict.
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        for member, label in zip(cls.__members__.values(), labels):
            member._label_ = label
        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    @property
    def names(cls):
        return tuple(member.name for member in cls)

    @property
    def choices(cls):
        return tuple((member.name, member.label) for member in cls)

    @property
    def labels(cls):
        return tuple(label for _, label in cls.choices)

    @property
    def values(cls):
        return tuple(value for value, _ in cls.choices)

    @property
    def options(cls):
        return tuple({"value": value, "text": text} for value, text in cls.choices)

    @property
    def mapping(cls):
        return dict(tuple(cls.choices))


class Choices(enum.Enum, metaclass=ChoicesMeta):
    """Class for creating enumerated choices."""

    @types.DynamicClassAttribute
    def label(self):
        return self._label_

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return super().__eq__(other)
        return self.value == other

    def __hash__(self):
        return hash(self._name_)


def restrict_to_permitted_evaluations(user, evaluations_qs):
    evals_for_user_qs = evaluations_qs.filter(users__in=[user])
    public_evals_qs = evaluations_qs.filter(visibility=choices.EvaluationVisibility.PUBLIC.value)
    restricted_evaluations_qs = evals_for_user_qs | public_evals_qs
    if not user.is_external_user:
        civil_service_evals_qs = evaluations_qs.filter(visibility=choices.EvaluationVisibility.CIVIL_SERVICE.value)
        restricted_evaluations_qs = civil_service_evals_qs | restricted_evaluations_qs
    return restricted_evaluations_qs


def check_evaluation_view_permission(func):
    @login_required
    def wrapper(request, *args, **kwargs):
        evaluation_id = kwargs["evaluation_id"]
        evaluation = models.Evaluation.objects.get(pk=evaluation_id)
        evaluation_users = evaluation.users.all()
        civil_service_user = not request.user.is_external_user
        evaluation_is_public = evaluation.visibility == choices.EvaluationVisibility.PUBLIC.value
        evaluation_is_civil_service = evaluation.visibility == choices.EvaluationVisibility.CIVIL_SERVICE.value
        if evaluation_is_public:
            return func(request, *args, **kwargs)
        elif evaluation_is_civil_service and civil_service_user:
            return func(request, *args, **kwargs)
        else:
            if request.user not in evaluation_users:
                raise Http404("Evaluation not found")
            return func(request, *args, **kwargs)

    return wrapper


def check_is_civil_service_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_external_user:
            raise Http404()
        return func(request, *args, **kwargs)

    return wrapper


def is_civil_service_email(email):
    allowed = False
    email = email.lower()
    email_split = email.split("@")
    if email_split[-1] in ALLOWED_CIVIL_SERVICE_DOMAINS:
        allowed = True
    return allowed
