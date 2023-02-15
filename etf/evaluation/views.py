import marshmallow
from allauth.account.views import SignupView
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import models, schemas


class MethodDispatcher:
    def __new__(cls, request, *args, **kwargs):
        view = super().__new__(cls)
        method_name = request.method.lower()
        method = getattr(view, method_name, None)
        if method:
            return method(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request)


class CustomSignupView(SignupView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            if models.User.objects.filter(email=request.POST.get("email")).exists():
                messages.error(request, "A user with this email already exists, please try again.")
                return render(request, self.template_name)
            form = self.get_form()
            if not form.is_valid():
                for field, error in form.errors.items():
                    messages.error(request, error)
                return render(request, self.template_name, {"form": form})
            if form.is_valid():
                try:
                    self.form_valid(form)
                except ValidationError as e:
                    messages.error(request, str(e))
                    return render(request, self.template_name, {"form": form})
        response = super().dispatch(request, *args, **kwargs)
        return response


@login_required
def index_view(request):
    if request.method == "POST":
        user = request.user
        evaluation = models.Evaluation.objects.create()
        evaluation.users.add(user)
        evaluation.save()
        return redirect(
            intro_page_view,
            evaluation_id=str(evaluation.id),
        )
    return render(request, "index.html")


def make_evaluation_url(evaluation_id, page_name):
    if not page_name:
        return None
    return reverse(page_name, args=(evaluation_id,))


def get_adjacent_outcome_measure_id(evaluation_id, outcome_measure_id, next_or_prev="next"):
    adjacent_id = None
    direction_map = {"next": 1, "prev": -1}
    outcomes_for_eval = models.OutcomeMeasure.objects.filter(evaluation__id=evaluation_id).order_by("id")
    outcomes_ids = list(outcomes_for_eval.values_list("id", flat=True))
    num_outcomes = len(outcomes_ids)
    current_index = outcomes_ids.index(outcome_measure_id)
    adjacent_index = current_index + direction_map[next_or_prev]
    if 0 <= adjacent_index < num_outcomes:
        adjacent_id = outcomes_ids[adjacent_index]
    return adjacent_id


@login_required
def simple_page_view(request, evaluation_id, page_data):
    prev_url = make_evaluation_url(evaluation_id, page_data["prev_page"])
    next_url = make_evaluation_url(evaluation_id, page_data["next_page"])
    page_name = page_data["page_name"]
    template_name = f"{page_name}.html"
    title = page_data["title"]
    form_data = {"title": title, "prev_url": prev_url, "next_url": next_url}
    return render(request, template_name, form_data)


def add_outcome_measure(evaluation_id):
    evaluation = models.Evaluation.objects.get(pk=evaluation_id)
    outcome = models.OutcomeMeasure(evaluation=evaluation)
    outcome.save()
    return redirect(reverse("outcome-measure-page", args=(evaluation_id, outcome.id)))


@login_required
def initial_outcome_measure_page_view(request, evaluation_id):
    errors = {}
    data = {}
    prev_url = reverse("description", args=(evaluation_id,))
    next_url = reverse("end", args=(evaluation_id,))
    if request.method == "POST":
        if "add" in request.POST:
            return add_outcome_measure(evaluation_id)
        return redirect(next_url)
    return render(
        request, "outcome-measures.html", {"errors": errors, "data": data, "prev_url": prev_url, "next_url": next_url}
    )


@login_required
def first_last_outcome_measure_view(request, evaluation_id, first_or_last="first"):
    outcomes_for_eval = models.OutcomeMeasure.objects.filter(evaluation__id=evaluation_id)
    if first_or_last == "first":
        outcomes_for_eval = outcomes_for_eval.order_by("id")
    else:
        outcomes_for_eval = outcomes_for_eval.order_by("-id")
    if outcomes_for_eval:
        outcome_id = outcomes_for_eval[0].id
        return redirect(reverse("outcome-measure-page", args=(evaluation_id, outcome_id)))
    else:
        return redirect(reverse("outcome-measures", args=(evaluation_id,)))


@login_required
def first_outcome_measure_page_view(request, evaluation_id):
    return first_last_outcome_measure_view(request, evaluation_id, first_or_last="first")


@login_required
def last_outcome_measure_page_view(request, evaluation_id):
    return first_last_outcome_measure_view(request, evaluation_id, first_or_last="last")


@login_required
def evaluation_view(request, evaluation_id, page_data):
    title = page_data["title"]
    page_name = page_data["page_name"]
    next_url = make_evaluation_url(evaluation_id, page_data["next_page"])
    prev_url = make_evaluation_url(evaluation_id, page_data["prev_page"])
    template_name = f"{page_name}.html"
    evaluation = models.Evaluation.objects.get(pk=evaluation_id)
    eval_schema = schemas.EvaluationSchema(unknown=marshmallow.EXCLUDE)
    errors = {}
    topics = models.Topic.choices
    organisations = models.Organisation.choices
    statuses = models.EvaluationStatus.choices
    if request.method == "POST":
        data = request.POST
        try:
            serialized_evaluation = eval_schema.load(data=data, partial=True)
            for field_name in serialized_evaluation:
                setattr(evaluation, field_name, serialized_evaluation[field_name])
            if "topics" in data.keys():
                topic_list = data.getlist("topics") or None
                setattr(evaluation, "topics", topic_list)
            if "organisations" in data.keys():
                organisation_list = data.getlist("organisations") or None
                setattr(evaluation, "organisations", organisation_list)
            evaluation.save()
            return redirect(next_url)
        except marshmallow.exceptions.ValidationError as err:
            errors = dict(err.messages)
    else:
        data = eval_schema.dump(evaluation)
    return render(
        request,
        template_name,
        {
            "errors": errors,
            "topics": topics,
            "organisations": organisations,
            "statuses": statuses,
            "data": data,
            "next_url": next_url,
            "prev_url": prev_url,
            "title": title,
        },
    )


@login_required
def outcome_measure_page_view(request, evaluation_id, outcome_measure_id):
    outcome = models.OutcomeMeasure.objects.get(id=outcome_measure_id)
    outcome_schema = schemas.OutcomeMeasureSchema(unknown=marshmallow.EXCLUDE)
    errors = {}
    data = {}
    show_add = False
    next_outcome_id = get_adjacent_outcome_measure_id(evaluation_id, outcome_measure_id, next_or_prev="next")
    prev_outcome_id = get_adjacent_outcome_measure_id(evaluation_id, outcome_measure_id, next_or_prev="prev")
    if next_outcome_id:
        next_url = reverse("outcome-measure-page", args=(evaluation_id, next_outcome_id))
    else:
        next_url = reverse("end", args=(evaluation_id,))
        show_add = True
    if prev_outcome_id:
        prev_url = reverse("outcome-measure-page", args=(evaluation_id, prev_outcome_id))
    else:
        prev_url = reverse("description", args=(evaluation_id,))
    if request.method == "POST":
        data = request.POST
        try:
            if "delete" in request.POST:
                delete_url = reverse("outcome-measure-delete", args=(evaluation_id, outcome_measure_id))
                return redirect(delete_url)
            serialized_outcome = outcome_schema.load(data=data, partial=True)
            for field_name in serialized_outcome:
                setattr(outcome, field_name, serialized_outcome[field_name])
            outcome.save()
            if "add" in request.POST:
                return add_outcome_measure(evaluation_id)
            return redirect(next_url)
        except marshmallow.exceptions.ValidationError as err:
            errors = dict(err.messages)
    else:
        data = outcome_schema.dump(outcome)
    return render(
        request,
        "outcome-measure-page.html",
        {"errors": errors, "data": data, "next_url": next_url, "prev_url": prev_url, "show_add": show_add},
    )


def delete_outcome_measure_page_view(request, evaluation_id, outcome_measure_id):
    outcome = models.OutcomeMeasure.objects.filter(evaluation__id=evaluation_id).get(id=outcome_measure_id)
    prev_id = get_adjacent_outcome_measure_id(evaluation_id, outcome_measure_id, next_or_prev="prev")
    outcome.delete()
    if prev_id:
        next_url = reverse("outcome-measure-page", args=(evaluation_id, prev_id))
    else:
        next_url = reverse("outcome-measures", args=(evaluation_id,))
    return redirect(next_url)


def intro_page_view(request, evaluation_id):
    page_data = {"title": "Introduction", "page_name": "intro", "prev_page": None, "next_page": "title"}
    return simple_page_view(request, evaluation_id, page_data)


def evaluation_title_view(request, evaluation_id):
    page_data = {"title": "Title", "page_name": "title", "prev_page": "intro", "next_page": "description"}
    return evaluation_view(request, evaluation_id, page_data)


def evaluation_description_view(request, evaluation_id):
    page_data = {
        "title": "Description",
        "page_name": "description",
        "prev_page": "title",
        "next_page": "outcome-measure-first",
    }
    return evaluation_view(request, evaluation_id, page_data)


def end_page_view(request, evaluation_id):
    page_data = {"title": "End", "page_name": "end", "prev_page": "outcome-measure-last", "next_page": None}
    return simple_page_view(request, evaluation_id, page_data)


class EvaluationSearchForm(forms.Form):
    id = forms.UUIDField(required=False)
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=100, required=False)
    topics = forms.MultipleChoiceField(choices=models.Topic.choices, required=False)
    organisations = forms.MultipleChoiceField(choices=models.Organisation.choices, required=False)
    status = forms.ChoiceField(choices=(("", "-----"), *models.EvaluationStatus.choices), required=False)
    search_phrase = forms.CharField(max_length=100, required=False)
    mine_only = forms.BooleanField(required=False)
    is_search = forms.CharField(max_length=6, required=True)


@login_required
def search_evaluations_view(request):
    qs = models.Evaluation.objects.all()
    data = {}
    errors = {}
    if request.method == "GET":
        form = EvaluationSearchForm(request.GET)
        if form.is_valid() and form.cleaned_data["is_search"]:
            topics = form.cleaned_data["topics"]
            organisations = form.cleaned_data["organisations"]
            status = form.cleaned_data["status"]
            search_phrase = form.cleaned_data["search_phrase"]
            mine_only = form.cleaned_data["mine_only"]
            if mine_only:
                qs = qs.filter(users__in=[request.user])
            if organisations:
                organisations_qs = models.Evaluation.objects.none()
                for organisation in organisations:
                    organisation_qs = qs.filter(organisations__contains=organisation)
                    organisations_qs = organisations_qs | organisation_qs
                qs = organisations_qs
            if not status:
                qs = qs.filter(
                    Q(status=models.EvaluationStatus.DRAFT.value, users__in=[request.user])
                    | Q(status__in=[models.EvaluationStatus.PUBLIC.value, models.EvaluationStatus.CIVIL_SERVICE.value])
                )
            else:
                if status == models.EvaluationStatus.DRAFT:
                    qs = qs.filter(status=status)
                    qs = qs.filter(user=request.user)
                # TODO: make civil service and public filter more sophisticated once roles are in
                if status == models.EvaluationStatus.PUBLIC:
                    qs = qs.filter(status=status)
                if status == models.EvaluationStatus.CIVIL_SERVICE:
                    qs = qs.filter(status=status)
            if topics:
                topics_qs = models.Evaluation.objects.none()
                for topic in topics:
                    topic_qs = qs.filter(topics__contains=topic)
                    topics_qs = topics_qs | topic_qs
                qs = topics_qs
            if search_phrase:
                # TODO - what fields do we care about?
                most_important_fields = ["id", "title", "description", "topics", "organisations"]
                other_fields = [
                    "issue_description",
                    "those_experiencing_issue",
                    "why_improvements_matter",
                    "who_improvements_matter_to",
                    "current_practice",
                    "issue_relevance",
                ]
                search_vector = SearchVector(most_important_fields[0], weight="A")
                for field in most_important_fields[1:]:
                    search_vector = search_vector + SearchVector(field, weight="A")
                for field in other_fields:
                    search_vector = search_vector + SearchVector(field, weight="B")
                search_query = SearchQuery(search_phrase)
                rank = SearchRank(search_vector, search_query)
                qs = qs.annotate(search=search_vector).annotate(rank=rank).filter(search=search_query).order_by("-rank")
            return render(request, "search-results.html", {"evaluations": qs, "errors": errors, "data": data})

        else:
            data = request.GET
            errors = form.errors
    return render(request, "search-form.html", {"form": form, "evaluations": qs, "errors": errors, "data": data})


@login_required
def my_evaluations_view(request):
    data = {}
    errors = {}
    if request.method == "GET":
        qs = models.Evaluation.objects.filter(users__in=[request.user])
        data = request.GET
    return render(request, "my-evaluations.html", {"evaluations": qs, "errors": errors, "data": data})


@login_required
@require_http_methods(["GET", "POST", "DELETE"])
class EvaluationContributor(MethodDispatcher):
    def get(self, request, evaluation_id):
        return render(request, "add-contributor.html", {"evaluation_id": evaluation_id})

    def post(self, request, evaluation_id):
        evaluation = models.Evaluation.objects.get(pk=evaluation_id)
        email = request.POST.get("add-user-email")
        user = models.User.objects.get(email=email)
        evaluation.users.add(user)
        evaluation.save()
        users = evaluation.users.values()
        return render(request, "contributor-rows.html", {"contributors": users, "evaluation_id": evaluation_id})

    def delete(self, request, evaluation_id, email_to_remove=None):
        evaluation = models.Evaluation.objects.get(pk=evaluation_id)
        user_to_remove = models.User.objects.get(email=email_to_remove)
        evaluation.users.remove(user_to_remove)
        evaluation.save()
        users = evaluation.users.values()
        if user_to_remove == request.user:
            response = render(
                request,
                "contributor-rows.html",
                {"redirect": True, "contributors": users, "evaluation_id": evaluation_id},
            )
            response["HX-Redirect"] = reverse("index")
            return response
        return render(request, "contributor-rows.html", {"contributors": users, "evaluation_id": evaluation_id})


@login_required
@require_http_methods(["POST"])
def evaluation_contributor_add_view(request, evaluation_id):
    evaluation = models.Evaluation.objects.get(pk=evaluation_id)
    email = request.POST.get("add-user-email")
    user = models.User.objects.get(email=email)
    evaluation.users.add(user)
    evaluation.save()
    return redirect(reverse("evaluation-contributors", args=(evaluation_id,)))


@login_required
@require_http_methods(["POST", "GET"])
def evaluation_contributor_remove_view(request, evaluation_id, email_to_remove=None):
    evaluation = models.Evaluation.objects.get(pk=evaluation_id)
    if request.method == "GET":
        return render(request, "remove-contributor.html", {"evaluation_id": evaluation_id, "email": email_to_remove})
    elif request.method == "POST":
        email = request.POST.get("remove-user-email")
        user = models.User.objects.get(email=email)
        evaluation.users.remove(user)
        evaluation.save()
        if user == request.user:
            return redirect(reverse("index"))
        return redirect(reverse("evaluation-contributors", args=(evaluation_id,)))


@login_required
def evaluation_summary_view(request, evaluation_id):
    evaluation = models.Evaluation.objects.get(pk=evaluation_id)
    user_can_edit = request.user in evaluation.users.all()
    return render(request, "evaluation-summary.html", {"data": evaluation, "user_can_edit": user_can_edit})
