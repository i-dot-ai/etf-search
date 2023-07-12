import functools

from nose.tools import with_setup

from eva_reg.evaluation import choices, enums, models

from . import utils


def setup_eval():
    user, _ = models.User.objects.get_or_create(email="peter.rabbit@example.com")
    user.set_password("pink-elephant")
    user.save()
    evaluation = models.Evaluation(title="An Evaluation")
    evaluation.save()
    evaluation.users.add(user)
    for i in range(3):
        name = f"Outcome measure {i}"
        outcome_measure = models.OutcomeMeasure(name=name, evaluation=evaluation)
        outcome_measure.save()
    other_measure = models.OtherMeasure(name="Other measure 1", evaluation=evaluation)
    other_measure.save()
    intervention = models.Intervention(name="Intervention 1", evaluation=evaluation)
    intervention.save()
    for i in range(2):
        name = f"Process {i}"
        process = models.ProcessStandard(name=name, evaluation=evaluation)
        process.save()


def teardown_eval():
    user = models.User.objects.get(email="peter.rabbit@example.com")
    user.delete()


@utils.with_authenticated_client
@with_setup(setup_eval, teardown_eval)
def test_evaluation_urls(client):
    user = models.User.objects.get(email="peter.rabbit@example.com")
    evaluation = user.evaluations.all()[0]
    urls_to_test = [
        f"evaluation/{evaluation.id}/",
        f"evaluation/{evaluation.id}/title",
        f"evaluation/{evaluation.id}/description",
        f"evaluation/{evaluation.id}/end",
    ]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200


@utils.with_authenticated_client
@with_setup(setup_eval, teardown_eval)
def test_outcome_measure_urls(client):
    user = models.User.objects.get(email="peter.rabbit@example.com")
    evaluation = user.evaluations.all()[0]
    outcome_measure = models.OutcomeMeasure.objects.filter(evaluation=evaluation).first()
    urls_to_test = [
        f"evaluation/{evaluation.id}/outcome-measures/",
        f"evaluation/{evaluation.id}/outcome-measures/{outcome_measure.id}/",
    ]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200


@utils.with_authenticated_client
@with_setup(setup_eval, teardown_eval)
def test_other_measure_urls(client):
    user = models.User.objects.get(email="peter.rabbit@example.com")
    evaluation = user.evaluations.all()[0]
    other_measure = models.OtherMeasure.objects.filter(evaluation=evaluation).first()
    urls_to_test = [
        f"evaluation/{evaluation.id}/other-measures/",
        f"evaluation/{evaluation.id}/other-measures/{other_measure.id}/",
    ]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200


@utils.with_authenticated_client
@with_setup(setup_eval, teardown_eval)
def test_intervention_measure_urls(client):
    user = models.User.objects.get(email="peter.rabbit@example.com")
    evaluation = user.evaluations.all()[0]
    intervention = models.Intervention.objects.filter(evaluation=evaluation).first()
    urls_to_test = [
        f"evaluation/{evaluation.id}/interventions/",
        f"evaluation/{evaluation.id}/interventions/{intervention.id}/",
    ]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200


@utils.with_authenticated_client
@with_setup(setup_eval, teardown_eval)
def test_processes_standards_measure_urls(client):
    user = models.User.objects.get(email="peter.rabbit@example.com")
    evaluation = user.evaluations.all()[0]
    process = models.ProcessStandard.objects.filter(evaluation=evaluation).first()
    urls_to_test = [
        f"evaluation/{evaluation.id}/processes-standards/",
        f"evaluation/{evaluation.id}/processes-standards/{process.id}/",
    ]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200


def _make_simple_step(title, fields, evaluation_id):
    return functools.partial(complete_verify_simple_page, title=title, fields=fields, evaluation_id=evaluation_id)


def _make_multple_object_step(title, new_item_name, added_item_name, fields):
    return functools.partial(
        complete_verify_multiple_object_page,
        title=title,
        new_item_name=new_item_name,
        added_item_name=added_item_name,
        fields=fields,
    )


def test_step_through_evaluation():
    # Setup evaluation
    test_email = "test-evaluation-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)
    evaluation = models.Evaluation.objects.create(title="Test evaluation")
    evaluation.save()
    user.evaluations.add(evaluation)
    user.save()
    intro_page = client.get(f"/evaluation/{evaluation.id}/")

    # Intro page
    assert intro_page.status_code == 200, intro_page.status_code
    assert intro_page.has_text("Enter your evaluation")
    assert intro_page.has_text("Next")
    page = intro_page.click(contains="Next")

    steps = [
        # Title page
        _make_simple_step("Title", {"title": "Test evaluation title"}, evaluation.id),
        # Option page
        _make_simple_step(
            "Optional information",
            {"issue_description_option": "YES", "ethics_option": "YES", "grants_option": "YES"},
            evaluation.id,
        ),
        # Description page
        _make_simple_step(
            "Description",
            {
                "brief_description": "A brief description of the evaluation",
                "organisations": [enums.Organisation.choices[0][0]],
            },
            evaluation.id,
        ),
        # Issue description page
        _make_simple_step(
            "Issue description",
            {
                "issue_description": "A brief description of the evaluation issue",
                "those_experiencing_issue": "The people who are experiencing this issue",
                "why_improvements_matter": "A statement about why the improvements matter",
                "who_improvements_matter_to": "A summary of the peoples the improvements matter to",
                "current_practice": "What the current practice is in relation to the issue",
                "issue_relevance": "How relevant is the issue to society",
            },
            evaluation.id,
        ),
        # Studied population page
        _make_simple_step(
            "Studied population",
            {
                "studied_population": "A brief description of the target population",
                "eligibility_criteria": "The criteria the population have to meet to be included",
                "sample_size": 1000,
                "sample_size_units": "A unit of measurement",
                "sample_size_details": "Any details about the same size",
            },
            evaluation.id,
        ),
        # Participant recruitment page
        _make_simple_step(
            "Participant recruitment",
            {
                "process_for_recruitment": "A summary of the process for recruitment",
                "recruitment_schedule": "A recruitment schedule",
            },
            evaluation.id,
        ),
        # Evaluation costs page
        _make_multple_object_step(
            "Evaluation costs and budget",
            "New evaluation cost",
            "An example evaluation cost",
            {
                "item_name": "An example evaluation cost",
                "description": "A description of the expense item",
                "item_cost": str(1000.0),
                "earliest_spend_date": "2022-03-07",
                "latest_spend_date": "2022-03-07",
            },
        ),
        # Evaluation types page
        _make_simple_step(
            "Evaluation types",
            {
                "evaluation_type": [
                    choices.EvaluationTypeOptions.ECONOMIC.value,
                    # TODO - readd tests for PROCESS evaluations
                    # choices.EvaluationTypeOptions.PROCESS.value,
                    choices.EvaluationTypeOptions.IMPACT.value,
                    choices.EvaluationTypeOptions.OTHER.value,
                ],
            },
            evaluation.id,
        ),
        # Event dates page
        _make_multple_object_step(
            "Event dates",
            "New event date",
            choices.EventDateOption.INTERVENTION_END_DATE.label,
            {
                "event_date_name": choices.EventDateOption.INTERVENTION_END_DATE.value,
                "date": "2022-03-07",
                "event_date_type": choices.EventDateType.ACTUAL.value,
            },
        ),
        # Impact evaluation design page
        _make_simple_step(
            "Impact evaluation design",
            {
                "impact_design_name": [choices.ImpactEvalDesign.REALISE_EVALUATION.value],
                "impact_design_justification": "A justification for the design",
                "impact_design_description": "A description of the design used",
                "impact_design_features": "The main features that the design offers",
                "impact_design_equity": "The equity of the design",
                "impact_design_assumptions": "The assumptions made based on this design",
                "impact_design_approach_limitations": "The limitations of this design approach",
            },
            evaluation.id,
        ),
        # Impact evaluation analysis page
        _make_simple_step(
            "Impact evaluation analysis",
            {
                "impact_framework": choices.ImpactFramework.EQUIVALENCE.value,
                "impact_basis": choices.ImpactAnalysisBasis.INTENTION_TO_TREAT.value,
                "impact_analysis_set": "Analysis set",
                "impact_effect_measure_type": choices.ImpactMeasureType.ABSOLUTE.value,
                "impact_primary_effect_size_measure": "Primary effect size measure",
                "impact_effect_measure_interval": choices.ImpactMeasureInterval.BAYESIAN.value,
                "impact_primary_effect_size_desc": "A description of the primary effect size measure",
                "impact_interpretation_type": choices.ImpactInterpretationType.NONE,
                "impact_sensitivity_analysis": "The sensitivity analysis",
                "impact_subgroup_analysis": "A subgroup analysis",
                "impact_missing_data_handling": "A summary of missing data handling",
                "impact_fidelity": "YES",
                "impact_description_planned_analysis": "The planned analysis of the impact",
            },
            evaluation.id,
        ),
        # TODO - add process evaluation design pages
        # Economic design page
        _make_simple_step(
            "Economic evaluation design",
            {
                "economic_type": choices.EconomicEvaluationType.COST_BENEFIT_ANALYSIS.value,
                "perspective_costs": "The perspective costs of the evaluation",
                "perspective_benefits": "The benefits associated with the evaluation",
                "monetisation_approaches": "The approach to monetisation",
                "economic_design_details": "Any details about the economic evaluation design",
            },
            evaluation.id,
        ),
        # Economic analysis page
        _make_simple_step(
            "Economic evaluation design",
            {"economic_analysis_description": "Description of the economic analysis"},
            evaluation.id,
        ),
        # Other design page
        _make_simple_step(
            "Other evaluation design",
            {
                "other_design_type": "The other evaluation design type",
                "other_design_details": "A description of the other design type",
            },
            evaluation.id,
        ),
        # Other analysis page
        _make_simple_step(
            "Other evaluation analysis",
            {
                "other_analysis_description": "A description of the other analysis",
            },
            evaluation.id,
        ),
        # Interventions page
        _make_multple_object_step(
            "Interventions",
            "New intervention",
            "Intervention name",
            {
                "name": "Intervention name",
                "brief_description": "A brief description of the intervention",
                "rationale": "The rationale behind the intervention",
                "materials_used": "The materials to be used in the intervention",
                "procedures": "The procedures to be used in the intervention",
                "provider_description": "A description of the provider of the intervention",
                "modes_of_delivery": "The modes of delivery used in the intervention",
                "location": "The location to be used for the intervention",
                "frequency_of_delivery": "The frequency of delivery for the intervention",
                "tailoring": "How is the intervention tailored to suit the needs",
                "fidelity": "The fidelity of the intervention",
                "resource_requirements": "The requirements for this intervention in resource costs",
                "geographical_information": "Any geographical information relevant to this intervention",
            },
        ),
        # Outcome measures page
        _make_multple_object_step(
            "Outcome measures",
            "New outcome measure",
            "Outcome measure name",
            {
                "name": "Outcome measure name",
                "primary_or_secondary": "PRIMARY",
                "direct_or_surrogate": "DIRECT",
                "measure_type": choices.MeasureType.BINARY.value,
                "description": "The description of the outcome measure",
                "collection_process": "The collection process for this outcome measure",
                "timepoint": "The process timings of interest",
                "minimum_difference": "The minimum practically important difference",
                "relevance": "The relevance of this outcome measure",
            },
        ),
        # Other measures page
        _make_multple_object_step(
            "Other measures",
            "New other measure",
            "Other measure name",
            {
                "name": "Other measure name",
                "measure_type": choices.MeasureType.BINARY.value,
                "description": "A description of the other measure",
                "collection_process": "The process of collection and timings",
            },
        ),
        # Ethics page
        _make_simple_step(
            "Ethics",
            {
                "ethics_committee_approval": "YES",
                "ethics_committee_details": "Details about the ethical committee",
                "ethical_state_given_existing_evidence_base": "Ethical state of study given existing evidence base",
                "risks_to_participants": "The risks to participants of the evaluation",
                "risks_to_study_team": "The risks to the team carrying out the evaluation",
                "participant_involvement": "The involvement of those taking part in the evaluation",
                "participant_consent": "What consent has obtained from the participants",
                "participant_information": "Information about the participants of this evaluation",
                "participant_payment": "Any payment the participants are receiving for taking part in the evaluation",
                "confidentiality_and_personal_data": "Details about the confidentiality of participant data",
                "breaking_confidentiality": "Information on what happens if confidentiality is broken",
                "other_ethical_information": "Any other notes about ethical topics relating to this evaluation",
            },
            evaluation.id,
        ),
        # Impact evaluation findings page
        _make_simple_step(
            "Impact evaluation findings",
            {
                "impact_comparison": "An evaluation comparison",
                "impact_outcome": "The outcome of the evaluation findings",
                "impact_interpretation": choices.ImpactEvalInterpretation.EQUIVALENCE_EQUIVALENT.value,
                "impact_point_estimate_diff": "The point estimate difference of the evaluation findings",
                "impact_lower_uncertainty": "The lower uncertainty of the evaluation findings",
                "impact_upper_uncertainty": "The upper uncertainty of the evaluation findings",
                "impact_summary_findings": "Summary findings",
                "impact_findings": "Impact findings",
            },
            evaluation.id,
        ),
        # Economic evaluation findings page
        _make_simple_step(
            "Economic evaluation findings",
            {
                "economic_summary_findings": "A summary of the economic findings of the evaluation",
                "economic_findings": "The findings of the evaluation",
            },
            evaluation.id,
        ),
        # TODO - readd process evaluation pages
        # Process evaluation findings page
        # _make_simple_step("Process evaluation findings", {}, evaluation.id),
        # Other evaluation findings page
        _make_simple_step(
            "Other evaluation findings",
            {
                "other_summary_findings": "The summary other findings of the evaluation",
                "other_findings": "The other findings of the evaluation",
            },
            evaluation.id,
        ),
        # Processes standards page
        _make_multple_object_step(
            "Processes and standards",
            "New process or standard",
            "New example process standard",
            {
                "name": "New example process standard",
                "conformity": "FULL",
                "description": "A description of the process or standard",
            },
        ),
        # Grants
        _make_multple_object_step(
            title="Grants",
            new_item_name="New grant",
            added_item_name="Grant 47",
            fields={"name_of_grant": "Grant 47", "grant_number": "REF47", "grant_details": "Loads more grant info"},
        ),
        # Links page
        _make_multple_object_step(
            "Links to other service",
            "New link",
            "New example link",
            {
                "name_of_service": "New example link",
                "link_or_identifier": "https://example.com",
            },
        ),
        # Status page
        _make_simple_step(
            "Evaluation visibility",
            {
                "visibility": choices.EvaluationVisibility.CIVIL_SERVICE.value,
            },
            evaluation.id,
        ),
    ]

    for step in steps:
        page = step(page)

    end_page = page
    # End page
    assert end_page.status_code == 200, end_page.status_code
    assert end_page.has_text("End")
    assert not end_page.has_text("Save and next")
    assert not end_page.has_text("Next")


def complete_verify_simple_page(page, title, fields, evaluation_id):
    assert page.status_code == 200, page.status_code
    assert page.has_text(title)
    assert page.has_text("Save and next")
    form = page.get_form("""form:not([action])""")

    extra_data = {}
    for field in fields:
        if isinstance(fields[field], (set, tuple, list)):
            extra_data[field] = fields[field]
        else:
            form[field] = fields[field]
    next_page = form.submit(extra=extra_data).follow()
    evaluation = models.Evaluation.objects.get(pk=evaluation_id)
    for field in fields:
        assert evaluation.__getattribute__(field) == fields[field], (getattr(evaluation, field), fields[field])
    return next_page


def complete_verify_multiple_object_page(page, title, new_item_name, added_item_name, fields):
    assert page.status_code == 200, page.status_code
    assert page.has_text(title)
    assert page.has_text("Next")
    add_item_form = page.get_form("""form:not([action])""")
    object_added_to_records_page = add_item_form.submit().follow()
    summary_page = object_added_to_records_page.click(contains="Cancel")
    assert summary_page.has_text(new_item_name), new_item_name
    editing_new_object_page = summary_page.click(contains=new_item_name)
    adding_new_item_form = editing_new_object_page.get_form("""form:not([action])""")
    for field in fields:
        adding_new_item_form[field] = fields[field]
    object_added_summary_page = adding_new_item_form.submit(extra={"return": ""}).follow()
    assert object_added_summary_page.has_text(added_item_name)
    deleting_object_page = object_added_summary_page.click(contains=added_item_name)
    deleting_object_form = deleting_object_page.get_form("""form:not([action])""")
    for field in fields:
        if isinstance(fields[field], list):
            assert deleting_object_form[field].__eq__(fields[field])
        else:
            assert deleting_object_form[field] == fields[field]
    object_deleted_summary_page = deleting_object_form.submit(extra={"delete": ""}).follow()
    assert object_deleted_summary_page.has_text(title)
    assert not object_deleted_summary_page.has_text(new_item_name)
    assert not object_deleted_summary_page.has_text(added_item_name)
    return object_deleted_summary_page.click(contains="Next")


@with_setup(setup_eval, teardown_eval)
def test_invite_collaborators():
    client = utils.make_testino_client()
    utils.register(client, email="test-contributors@example.com", password="pink-elephants")
    user = models.User.objects.get(email="test-contributors@example.com")
    evaluation = models.Evaluation.objects.first()
    evaluation.users.add(user)
    evaluation_id = evaluation.id
    contributor_page = client.get(f"/evaluation-contributors/{evaluation_id}/")
    assert contributor_page.status_code == 200
    # Check adding valid and invalid emails
    form = contributor_page.get_form("""form:not([action])""")
    form.set(field_name="email", value="nina@example.com")
    response = form.submit()
    assert response.status_code == 200
    assert response.has_text("nina@example.com")
    form = response.get_form("""form:not([action])""")
    form.set(field_name="email", value="invalid@example.org")
    response = form.submit()
    assert response.status_code == 200
    assert response.has_text("This should be a valid Civil Service email")
    assert not response.has_text("invalid@example.org")
