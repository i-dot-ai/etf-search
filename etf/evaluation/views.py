from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import choices, enums, models


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
    return render(request, "page-not-found.html", {})


def test_view(request, exception=None):
    return render(request, "beta/beta-test.html", {})


class EvaluationSearchForm(forms.Form):
    id = forms.UUIDField(required=False)
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=100, required=False)
    topics = forms.MultipleChoiceField(choices=choices.Topic.choices, required=False)
    organisations = forms.MultipleChoiceField(choices=enums.Organisation.choices, required=False)
    status = forms.ChoiceField(choices=(("", "-----"), *choices.EvaluationStatus.choices), required=False)
    search_phrase = forms.CharField(max_length=100, required=False)
    mine_only = forms.BooleanField(required=False)
    is_search = forms.CharField(max_length=6, required=True)


@login_required
@require_http_methods(["GET"])
class EvaluationSearchView(MethodDispatcher):
    def get(self, request):
        search_text = request.GET.get("search_text")
        organisations = request.GET.getlist("organisations")
        topics = request.GET.getlist("topics")
        evaluation_types = request.GET.getlist("evaluation_types")
        status = request.GET.getlist("status")
        current_url = request.get_full_path()

        qs = models.Evaluation.objects.all()

        if search_text:
            qs = qs.filter(title__contains=search_text)
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
        if not status:
            qs = qs.filter(
                Q(status=choices.EvaluationStatus.DRAFT.value, users__in=[request.user])
                | Q(status__in=[choices.EvaluationStatus.PUBLIC.value, choices.EvaluationStatus.CIVIL_SERVICE.value])
            )
        else:
            if status == choices.EvaluationStatus.DRAFT:
                qs = qs.filter(status=status)
                qs = qs.filter(users__in=[request.user])
            # TODO: make civil service and public filter more sophisticated once roles are in
            if status == choices.EvaluationStatus.PUBLIC:
                qs = qs.filter(status=status)
            if status == choices.EvaluationStatus.CIVIL_SERVICE:
                qs = qs.filter(status=status)

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

        status_filters = choices.EvaluationStatus.choices
        filtered_status_filters = [
            status_filter
            for status_filter in status_filters
            if status_filter[0] in status or any(status_filter[0] in i.status for i in qs)
        ]

        evaluation_types_filters = choices.EvaluationTypeOptions.choices
        filtered_evaluation_types_filters = [
            evaluation_types_filter
            for evaluation_types_filter in evaluation_types_filters
            if evaluation_types_filter[0] in evaluation_types or any(evaluation_types_filter[0] in i.status for i in qs)
        ]

        return render(
            request,
            "search-form.html",
            {
                "data": {
                    "evaluations": qs,
                    "statuses": filtered_status_filters,
                    "evaluation_types": filtered_evaluation_types_filters,
                    "topics": filtered_topics_filters,
                    "organisations": filtered_organisation_filters,
                    "selected_statuses": status or [],
                    "selected_evaluation_types": evaluation_types or [],
                    "selected_topics": topics or [],
                    "selected_organisations": organisations or [],
                    "search_text": search_text or "",
                    "current_url": current_url,
                },
            },
        )


# TODO - remove the old search views once the new stuff is up and running
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
                    Q(status=choices.EvaluationStatus.DRAFT.value, users__in=[request.user])
                    | Q(
                        status__in=[choices.EvaluationStatus.PUBLIC.value, choices.EvaluationStatus.CIVIL_SERVICE.value]
                    )
                )
            else:
                if status == choices.EvaluationStatus.DRAFT:
                    qs = qs.filter(status=status)
                    qs = qs.filter(user=request.user)
                # TODO: make civil service and public filter more sophisticated once roles are in
                if status == choices.EvaluationStatus.PUBLIC:
                    qs = qs.filter(status=status)
                if status == choices.EvaluationStatus.CIVIL_SERVICE:
                    qs = qs.filter(status=status)
            if topics:
                topics_qs = models.Evaluation.objects.none()
                for topic in topics:
                    topic_qs = qs.filter(topics__contains=topic)
                    topics_qs = topics_qs | topic_qs
                qs = topics_qs
            if search_phrase:
                # TODO - what fields do we care about?
                most_important_fields = ["id", "title", "brief_description", "topics", "organisations"]
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
