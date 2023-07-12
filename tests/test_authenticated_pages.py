from nose import with_setup

from eva_reg.evaluation import choices, fields, interface, models

from . import utils

OVERVIEW_URLS = [
    "/overview/",
    "/overview/measured/",
    "/overview/design/",
    "/overview/analysis/",
    "/overview/findings/",
    "/overview/cost/",
]


@utils.with_authenticated_client
def test_get_pages_logged_in(client):
    urls_to_test = ["/search/", "/my-evaluations/"]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200


def test_malformed_markdown():
    fields.description_help_text[
        "brief_description"
    ] = "Please provide</head> one or two sentences to describe</b> the evaluation."
    authenticated_user = {"email": "test-markdown@example.com", "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email="test-markdown@example.com")
    evaluation = models.Evaluation(title="An Evaluation with markdown helptext")
    evaluation.save()
    evaluation.users.add(user)
    fields.description_help_text[
        "brief_description"
    ] = "Please provide one or two sentences to describe the evaluation."
    response = client.get(f"evaluation/{evaluation.id}/description/")
    assert response.has_text("Please provide one or two sentences to describe the evaluation.")


@utils.with_authenticated_client
def test_evaluation_permissions(client):
    # Setup evaluation
    test_email = "test-evaluation-permissions@example.com"
    user, _ = models.User.objects.get_or_create(email=test_email)
    evaluation = models.Evaluation.objects.create(title="Test evaluation")
    evaluation.save()
    user.evaluations.add(evaluation)
    user.save()

    urls = (
        f"/evaluation/{evaluation.id}/",
        f"evaluation/{evaluation.id}/title/",
        f"evaluation/{evaluation.id}/description/",
        f"evaluation/{evaluation.id}/issue-description/",
        f"evaluation/{evaluation.id}/studied-population/",
        f"evaluation/{evaluation.id}/participant-recruitment/",
        f"evaluation/{evaluation.id}/policy-costs/",
        f"evaluation/{evaluation.id}/publication-intention/",
        f"evaluation/{evaluation.id}/evaluation-types/",
        f"evaluation/{evaluation.id}/impact-design/",
        f"evaluation/{evaluation.id}/impact-analysis/",
        f"evaluation/{evaluation.id}/process-design-aspects/",
        f"evaluation/{evaluation.id}/process-analysis/",
        f"evaluation/{evaluation.id}/economic-design/",
        f"evaluation/{evaluation.id}/economic-analysis/",
        f"evaluation/{evaluation.id}/other-design/",
        f"evaluation/{evaluation.id}/other-analysis/",
        f"evaluation/{evaluation.id}/ethics/",
        f"evaluation/{evaluation.id}/impact-findings/",
        f"evaluation/{evaluation.id}/economic-findings/",
        f"evaluation/{evaluation.id}/process-findings/",
        f"evaluation/{evaluation.id}/other-findings/",
        f"evaluation/{evaluation.id}/metadata/",
        f"evaluation/{evaluation.id}/visibility/",
        f"evaluation/{evaluation.id}/end/",
    )

    for url in urls:
        response = client.get(url)
        assert response.status_code == 404


def setup_evaluations():
    internal_user, _ = models.User.objects.get_or_create(email="internal@example.com")
    internal_user.save()
    external_user, _ = models.User.objects.get_or_create(email="jemima.puddleduck@example.org", is_external_user=True)
    external_user.save()
    public_evaluation = interface.facade.evaluation.create(user_id=internal_user.id)
    interface.facade.evaluation.update(
        user_id=internal_user.id,
        evaluation_id=public_evaluation["id"],
        data={"title": "Public", "visibility": choices.EvaluationVisibility.PUBLIC.value},
    )
    civil_service_evaluation = interface.facade.evaluation.create(user_id=internal_user.id)
    interface.facade.evaluation.update(
        user_id=internal_user.id,
        evaluation_id=civil_service_evaluation["id"],
        data={"title": "Civil Service", "visibility": choices.EvaluationVisibility.CIVIL_SERVICE.value},
    )

    draft_evaluation1 = interface.facade.evaluation.create(user_id=internal_user.id)
    interface.facade.evaluation.update(
        user_id=internal_user.id,
        evaluation_id=draft_evaluation1["id"],
        data={"title": "Draft 1", "visibility": choices.EvaluationVisibility.DRAFT.value},
    )
    draft_evaluation2 = interface.facade.evaluation.create(user_id=internal_user.id)
    interface.facade.evaluation.update(
        user_id=internal_user.id,
        evaluation_id=draft_evaluation2["id"],
        data={"title": "Draft 2", "visibility": choices.EvaluationVisibility.DRAFT.value},
    )
    peter_rabbit, _ = models.User.objects.get_or_create(email="peter.rabbit@example.com")
    # TODO change to use facade to add users to evaluation
    draft_evaluation_object = models.Evaluation.objects.get(id=draft_evaluation2["id"])
    draft_evaluation_object.users.add(peter_rabbit, external_user)


def teardown_evaluations():
    models.Evaluation.objects.filter(title__in=["Public", "Civil Service", "Draft 1", "Draft 2"]).delete()
    models.User.objects.filter(email__in=["internal@example.com"]).delete()


def get_evaluation_ids():
    public_eval = models.Evaluation.objects.get(title="Public")
    civil_service_eval = models.Evaluation.objects.get(title="Civil Service")
    draft_eval1 = models.Evaluation.objects.get(title="Draft 1")
    draft_eval2 = models.Evaluation.objects.get(title="Draft 2")
    evaluation_ids = {
        "public": public_eval.id,
        "civil_service": civil_service_eval.id,
        "draft_not_a_contributor": draft_eval1.id,
        "draft_contributor": draft_eval2.id,
    }
    return evaluation_ids


def check_overview_urls(client, evaluation_id, expected_status_code):
    for url in OVERVIEW_URLS:
        full_url = f"/evaluation-summary/{evaluation_id}{url}"
        response = client.get(full_url)
        assert response.status_code == expected_status_code


@utils.with_authenticated_client
@with_setup(setup_evaluations, teardown_evaluations)
def test_overview_internal_access(client):
    evaluation_ids = get_evaluation_ids()
    check_overview_urls(client, evaluation_ids["public"], expected_status_code=200)
    check_overview_urls(client, evaluation_ids["civil_service"], expected_status_code=200)
    check_overview_urls(client, evaluation_ids["draft_not_a_contributor"], expected_status_code=404)
    check_overview_urls(client, evaluation_ids["draft_contributor"], expected_status_code=200)


@utils.with_authenticated_external_client
@with_setup(setup_evaluations, teardown_evaluations)
def test_overview_external_access(client):
    evaluation_ids = get_evaluation_ids()
    check_overview_urls(client, evaluation_ids["public"], expected_status_code=200)
    check_overview_urls(client, evaluation_ids["civil_service"], expected_status_code=404)
    check_overview_urls(client, evaluation_ids["draft_not_a_contributor"], expected_status_code=404)
    check_overview_urls(client, evaluation_ids["draft_contributor"], expected_status_code=200)
