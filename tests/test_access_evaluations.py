"""
Tests to ensure can't access evaluation views if you don't have the right permissions.

Initial tests check all URLs and deliberate exclude some - this is so we ensure new
URLs get tested. You will have to be explicit about URLs that don't need to be tested (for access).
"""

from django.urls import reverse
from nose import with_setup

from eva_reg import urls
from eva_reg.evaluation import models

from . import utils

# Explicitly excluding URLs if they need different tests
# This is to ensure that we don't miss out new URLs
EDIT_OR_VIEW_EVALUATION_URL_PATTERNS = (
    set(urls.urlpatterns)
    - set(urls.initial_urlpatterns)
    - set(urls.account_urlpatterns)
    - set(urls.feedback_and_help_urlpatterns)
    - set(urls.terms_and_conditions_urlpatterns)
    - set(urls.debug_urlpatterns)
)

VIEW_EVALUATION_URL_PATTERNS = (
    set(urls.urlpatterns)
    - set(urls.initial_urlpatterns)
    - set(urls.account_urlpatterns)
    - set(urls.feedback_and_help_urlpatterns)
    - set(urls.terms_and_conditions_urlpatterns)
    - set(urls.evaluation_edit_patterns)
    - set(urls.debug_urlpatterns)
)

EDIT_EVALUATIONS = set(EDIT_OR_VIEW_EVALUATION_URL_PATTERNS) - set(VIEW_EVALUATION_URL_PATTERNS)

# Non-standard URLs to ignore by standard tests - explicitly write tests
NAMES_TO_IGNORE = ["evaluation-contributor-remove", "evaluation-overview", "create-evaluation"]


# URLs also get ignored - have explicitly written tests for these related objects
RELATED_OBJECTS = {
    "intervention-page": "Intervention",
    "outcome-measure-page": "OutcomeMeasure",
    "other-measure-page": "OtherMeasure",
    "processes-standard-page": "ProcessStandard",
    "evaluation-cost-page": "EvaluationCost",
    "document-page": "Document",
    "link-page": "LinkOtherService",
    "event-date-page": "EventDate",
    "grant-page": "Grant",
    "process-evaluation-method-page": "ProcessEvaluationMethod",
}


def get_url_for_evaluation_and_related_object(client, url_name, evaluation_id, related_id=None):
    if (url_name in NAMES_TO_IGNORE) or (url_name in RELATED_OBJECTS.keys()):
        return
    if related_id:
        url = reverse(url_name, args=(evaluation_id, related_id))
    else:
        url = reverse(url_name, args=(evaluation_id,))
    response = client.get(url)
    return response


def check_related_objects_status(client, evaluation, expected_status):
    for url_name, model_name in RELATED_OBJECTS.items():
        model = getattr(models, model_name)
        new_obj = model(evaluation=evaluation)
        new_obj.save()
        related_id = new_obj.id
        response = get_url_for_evaluation_and_related_object(client, url_name, evaluation.id, related_id)
        if response:
            assert response.status_code == expected_status, response.status_code


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_client
def test_cant_edit_or_view_evaluations(client):
    evaluation_draft = models.Evaluation.objects.filter(title="Draft evaluation 1").first()
    for url_pattern in EDIT_OR_VIEW_EVALUATION_URL_PATTERNS:
        response = get_url_for_evaluation_and_related_object(client, url_pattern.name, evaluation_draft.id)
    if response:
        assert response.status_code == 404, url_pattern.name


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_client
def test_cant_edit_or_view_related_objects(client):
    evaluation_draft = models.Evaluation.objects.filter(title="Draft evaluation 1").first()
    evaluation_cs = models.Evaluation.objects.filter(title="Civil Service evaluation 1").first()
    evaluation_public = models.Evaluation.objects.filter(title="Public evaluation 1").first()
    for evaluation in [evaluation_draft, evaluation_cs, evaluation_public]:
        check_related_objects_status(client, evaluation, expected_status=404)


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_client
def test_view_not_edit_evaluations(client):
    evaluation_cs = models.Evaluation.objects.filter(title="Civil Service evaluation 1").first()
    evaluation_public = models.Evaluation.objects.filter(title="Public evaluation 1").first()
    for evaluation in [evaluation_cs, evaluation_public]:
        for url_pattern in EDIT_EVALUATIONS:
            response = get_url_for_evaluation_and_related_object(client, url_pattern.name, evaluation.id)
            if response:
                assert response.status_code == 404, response.status_code
        for url_pattern in VIEW_EVALUATION_URL_PATTERNS:
            response = get_url_for_evaluation_and_related_object(client, url_pattern.name, evaluation.id)
            if response:
                assert response.status_code == 200, response.status_code


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_external_client
def test_cant_edit_or_view_evaluations_external(client):
    evaluation_draft = models.Evaluation.objects.filter(title="Draft evaluation 1").first()
    evaluation_cs = models.Evaluation.objects.filter(title="Civil Service evaluation 1").first()
    for evaluation in [evaluation_cs, evaluation_draft]:
        for url_pattern in EDIT_OR_VIEW_EVALUATION_URL_PATTERNS:
            response = get_url_for_evaluation_and_related_object(client, url_pattern.name, evaluation.id)
        if response:
            assert response.status_code == 404, url_pattern.name


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_external_client
def test_cant_edit_or_view_related_objects_external(client):
    evaluation_draft = models.Evaluation.objects.filter(title="Draft evaluation 1").first()
    evaluation_cs = models.Evaluation.objects.filter(title="Civil Service evaluation 1").first()
    evaluation_public = models.Evaluation.objects.filter(title="Public evaluation 1").first()
    for evaluation in [evaluation_draft, evaluation_cs, evaluation_public]:
        check_related_objects_status(client, evaluation, expected_status=404)


@utils.with_authenticated_external_client
def test_external_cant_create_evaluation(client):
    response = client.get(reverse("create-evaluation"))
    assert response.status_code == 404


@utils.with_authenticated_client
def test_internal_create_evaluation(client):
    response = client.get(reverse("create-evaluation"))
    assert response.status_code == 200


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_client
def test_internal_evaluation_overview(client):
    evaluation_draft = models.Evaluation.objects.filter(title="Draft evaluation 1").first()
    url = reverse("evaluation-overview", args=(evaluation_draft.id,))
    response = client.get(url)
    assert response.status_code == 404


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_external_client
def test_external_evaluation_overview(client):
    evaluation_draft = models.Evaluation.objects.filter(title="Draft evaluation 1").first()
    evaluation_cs = models.Evaluation.objects.filter(title="Civil Service evaluation 1").first()
    for evaluation in [evaluation_draft, evaluation_cs]:
        url = reverse("evaluation-overview", args=(evaluation.id,))
        response = client.get(url)
        assert response.status_code == 404


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_authenticated_external_client
def test_remove_contributor(client):
    evaluation = models.Evaluation.objects.filter(title="Civil Service evaluation 2").first()
    user = models.User.objects.get(email="jemima.puddleduck@example.org")
    evaluation.users.add(user)
    evaluation.save()
    url = reverse("evaluation-contributor-remove", args=(evaluation.id, "mrs.tiggywinkle@example.com"))
    response = client.get(url)
    assert response.status_code == 405, response.status_code


@with_setup(utils.create_fake_evaluations, utils.remove_fake_evaluations)
@utils.with_client
def test_anon_evaluation_overview(client):
    evaluation_draft = models.Evaluation.objects.filter(title="Draft evaluation 1").first()
    evaluation_cs = models.Evaluation.objects.filter(title="Civil Service evaluation 1").first()
    url_names = (
        "evaluation-summary-overview",
        "evaluation-summary-measured",
        "evaluation-summary-design",
        "evaluation-summary-analysis",
        "evaluation-summary-findings",
        "evaluation-summary-cost",
    )
    for evaluation in [evaluation_draft, evaluation_cs]:
        for url_name in url_names:
            url = reverse(url_name, args=(evaluation.id,))
        response = client.get(url)
        assert response.status_code == 302
        assert (
            response.headers["location"]
            == f"/accounts/login/?next=/evaluation-summary/{evaluation.id}/overview/{url_name.split('-')[-1]}/"
        )
