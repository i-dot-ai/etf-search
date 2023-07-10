from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError

from etf.evaluation import interface, schemas

from . import choices, enums, models
from .email_handler import send_contributor_added_email, send_invite_email
from .utils import (
    check_edit_evaluation_permission,
    restrict_to_permitted_evaluations,
)


class MethodDispatcher:
    def __new__(cls, request, *args, **kwargs):
        view = super().__new__(cls)
        method_name = request.method.lower()
        method = getattr(view, method_name, None)
        if method:
            return method(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request)


# Unused request and exception arguments are required by django 404 handler function
def view_404(request, exception=None):
    return render(request, "page-not-found.html", {}, status=404)


def beta_test_view(request, exception=None):
    return render(request, "beta/beta-test.html", {})


def get_search_filters(qs, organisations, topics, visibility, evaluation_types):
    organisation_filters = enums.Organisation.choices
    filtered_organisation_filters = [
        organisation_filter
        for organisation_filter in organisation_filters
        if organisation_filter[0] in organisations or any(organisation_filter[0] in i.organisations for i in qs)
    ]

    topic_filters = choices.Topic.choices
    filtered_topics_filters = [
        topic_filter
        for topic_filter in topic_filters
        if topic_filter[0] in topics or any(topic_filter[0] in i.topics for i in qs)
    ]

    visibility_filters = choices.EvaluationVisibility.choices
    filtered_visibility_filters = [
        visibility_filter
        for visibility_filter in visibility_filters
        if visibility_filter[0] in visibility or any(visibility_filter[0] in i.visibility for i in qs)
    ]

    evaluation_types_filters = choices.EvaluationTypeOptions.choices
    filtered_evaluation_types_filters = [
        evaluation_types_filter
        for evaluation_types_filter in evaluation_types_filters
        if evaluation_types_filter[0] in evaluation_types
        or any(evaluation_types_filter[0] in i.evaluation_type for i in qs)
    ]

    output = {
        "visibilities": filtered_visibility_filters,
        "evaluation_types": filtered_evaluation_types_filters,
        "topics": filtered_topics_filters,
        "organisations": filtered_organisation_filters,
    }
    return output


@login_required
@require_http_methods(["GET"])
class EvaluationSearchView(MethodDispatcher):
    def get(self, request):
        search_term = request.GET.get("search_term")
        organisations = request.GET.getlist("organisations")
        topics = request.GET.getlist("topics")
        evaluation_types = request.GET.getlist("evaluation_types")
        visibility = request.GET.getlist("visibility")
        active_filter = request.GET.get("active_filter")
        current_url = request.get_full_path()

        qs = models.Evaluation.objects.all()
        qs = restrict_to_permitted_evaluations(request.user, qs)
        total_evaluations = qs.count()

        if organisations:
            organisations_qs = models.Evaluation.objects.none()
            for organisation in organisations:
                organisation_qs = qs.filter(organisations__contains=organisation)
                organisations_qs = organisations_qs | organisation_qs
            qs = organisations_qs
        if topics:
            topics_qs = models.Evaluation.objects.none()
            for topic in topics:
                topic_qs = qs.filter(topics__contains=topic)
                topics_qs = topics_qs | topic_qs
            qs = topics_qs
        if evaluation_types:
            evaluation_types_qs = models.Evaluation.objects.none()
            for evaluation_type in evaluation_types:
                evaluation_type_qs = qs.filter(evaluation_type__contains=evaluation_type)
                evaluation_types_qs = evaluation_types_qs | evaluation_type_qs
            qs = evaluation_types_qs
        filters = get_search_filters(qs, organisations, topics, visibility, evaluation_types)
        if visibility:
            query = Q()
            if choices.EvaluationVisibility.DRAFT.value in visibility:
                query |= Q(visibility__contains=choices.EvaluationVisibility.DRAFT.value)
            if choices.EvaluationVisibility.PUBLIC.value in visibility:
                query |= Q(visibility__contains=choices.EvaluationVisibility.PUBLIC.value)
            if choices.EvaluationVisibility.CIVIL_SERVICE.value in visibility:
                query |= Q(visibility__contains=choices.EvaluationVisibility.CIVIL_SERVICE.value)
            qs = qs.filter(query)
        # For now, place the highest weight on title and description
        if search_term:
            search_vector = SearchVector("title", "brief_description", weight="A") + SearchVector(
                "search_text", weight="B"
            )
            search_query = SearchQuery(search_term)
            rank = SearchRank(search_vector, search_query)
            qs = qs.annotate(search=search_vector).annotate(rank=rank).filter(search=search_query).order_by("-rank")

        data = {
            "evaluations": qs,
            "visibilities": filters["visibilities"],
            "evaluation_types": filters["evaluation_types"],
            "topics": filters["topics"],
            "organisations": filters["organisations"],
            "selected_visibilities": visibility or [],
            "selected_evaluation_types": evaluation_types or [],
            "selected_topics": topics or [],
            "selected_organisations": organisations or [],
            "search_term": search_term or "",
            "current_url": current_url,
            "total_evaluations": total_evaluations,
            "active_filter": active_filter,
        }
        return render(
            request,
            "search-form.html",
            {"data": data},
        )


@login_required
def my_evaluations_view(request):
    data = {}
    errors = {}
    if request.method == "GET":
        evaluations = tuple(models.Evaluation.objects.filter(users__in=[request.user]).all())
        data = request.GET
    return render(request, "my-evaluations.html", {"evaluations": evaluations, "errors": errors, "data": data})


@login_required
@check_edit_evaluation_permission
@require_http_methods(["GET", "POST", "DELETE"])
class EvaluationContributor(MethodDispatcher):
    def get(self, request, evaluation_id):
        errors = {}
        evaluation = models.Evaluation.objects.get(pk=evaluation_id)
        users = evaluation.users.all()
        return render(
            request,
            "contributors/contributors.html",
            {"contributors": users, "evaluation": evaluation, "errors": errors},
        )

    def post(self, request, evaluation_id):
        errors = {}
        evaluation = models.Evaluation.objects.get(pk=evaluation_id)
        try:
            serialized_user_to_add = schemas.UserSchema().load(request.POST, unknown=EXCLUDE)
            output = interface.facade.evaluation.add_user_to_evaluation(
                user_id=request.user.id, evaluation_id=evaluation_id, user_to_add_data=serialized_user_to_add
            )
            user_added = models.User.objects.get(id=output["user_added_id"])
            if output["is_new_user"]:
                send_invite_email(user_added)
            else:
                send_contributor_added_email(user_added, evaluation_id)
        except ValidationError as err:
            errors = dict(err.messages)
        users = evaluation.users.all()
        return render(
            request,
            "contributors/contributors.html",
            {"contributors": users, "evaluation": evaluation, "errors": errors},
        )


@login_required
@check_edit_evaluation_permission
@require_http_methods(["POST"])
def evaluation_contributor_remove_view(request, evaluation_id, email_to_remove):
    if request.method == "POST":
        email = email_to_remove
        user_to_remove = models.User.objects.get(email=email)
        interface.facade.evaluation.remove_user_from_evaluation(
            user_id=request.user.id, evaluation_id=evaluation_id, user_to_remove_id=user_to_remove.id
        )
        if request.user == user_to_remove:
            return redirect("index")
        return redirect("evaluation-contributors", evaluation_id=evaluation_id)


@require_http_methods(["GET"])
def feedback_and_help_view(request):
    return render(request, "feedback-and-help.html", {"feedback_email": settings.FEEDBACK_EMAIL})


@require_http_methods(["GET"])
def terms_and_conditions_view(request):
    return render(request, "terms-and-conditions.html", {})
