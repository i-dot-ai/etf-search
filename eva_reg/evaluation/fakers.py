"""
Create fake evaluations for testing.
"""

import datetime
import random

import faker

from . import choices, enums, models
from .pages import get_default_page_statuses

fake = faker.Faker()


def make_random_date(range_start=-3 * 365, range_end=3 * 365):
    num_days = random.randint(range_start, range_end)
    date = datetime.date.today() + datetime.timedelta(days=num_days)
    return date


def random_days_later(start_date, range_start, range_end):
    delta = datetime.timedelta(random.randint(range_start, range_end))
    random_date = start_date + delta
    return random_date


def make_random_yes_no():
    yes_or_no = random.randint(0, 1)
    if yes_or_no == 0:
        return "NO"
    else:
        return "YES"


def make_fake_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    data = dict(
        first_name=first_name,
        last_name=first_name,
        email=f"{first_name}.{last_name}@example.com".lower(),
        is_active=True,
    )
    return data


def generate_topics():
    num_topics = random.randint(0, 4)
    set_topics = set()
    for i in range(num_topics):
        set_topics.add(random.choice(choices.Topic.values))
    return list(set_topics)


def generate_organisations():
    num_organisations = random.randint(0, 4)
    set_organisations = set()
    for i in range(num_organisations):
        set_organisations.add(random.choice(enums.Organisation.values))
    return list(set_organisations)


def generate_evaluation_types():
    num_types = random.randint(0, 2)
    set_types = set()
    for i in range(num_types):
        set_types.add(random.choice(choices.EvaluationTypeOptions.values))
    return list(set_types)


def generate_costs(evaluation):
    num_costs = random.randint(0, 4)
    set_costs = set()
    for i in range(num_costs):
        set_costs.add(
            models.EvaluationCost(
                item_cost=random.randint(0, 50_000),
                item_name=fake.text(),
                created_at=fake.date(),
                evaluation_id=evaluation.id,
                description=fake.text(),
                earliest_spend_date=fake.date(),
                latest_spend_date=fake.date(),
            )
        )
    models.EvaluationCost.objects.bulk_create(set_costs)


def generate_documents(evaluation):
    num_documents = random.randint(0, 4)
    set_documents = set()
    for i in range(num_documents):
        set_documents.add(
            models.Document(
                description=fake.text(),
                document_types=random.choices(choices.DocumentType.values),
                evaluation_id=evaluation.id,
                document_type_other=fake.text(256),
                title=fake.text(),
                url=fake.url(),
            )
        )
    models.Document.objects.bulk_create(set_documents)


def generate_dates(evaluation):
    num_dates = random.randint(0, 4)
    set_dates = set()
    for i in range(num_dates):
        set_dates.add(
            models.EventDate(
                evaluation_id=evaluation.id,
                event_date_name=random.choice(choices.EventDateOption.values),
                date=fake.date(),
                event_date_type=random.choice(choices.EventDateType.values),
            )
        )
    models.EventDate.objects.bulk_create(set_dates)


def generate_interventions(evaluation):
    num_interventions = random.randint(0, 4)
    set_interventions = set()
    for i in range(num_interventions):
        set_interventions.add(
            models.Intervention(
                evaluation_id=evaluation.id,
                fidelity=fake.text(),
                location=fake.address(),
                rationale=fake.text(),
                name=fake.text(1024),
                brief_description=fake.text(),
                materials_used=fake.text(),
                procedures=fake.text(),
                provider_description=fake.text(),
                modes_of_delivery=fake.text(),
                frequency_of_delivery=fake.text(),
                tailoring=fake.text(),
                resource_requirements=fake.text(),
                geographical_information=fake.text(),
            )
        )
    models.Intervention.objects.bulk_create(set_interventions)


def generate_outcome_measures(evaluation):
    num_outcome_measures = random.randint(0, 4)
    set_outcome_measures = set()
    for i in range(num_outcome_measures):
        set_outcome_measures.add(
            models.OutcomeMeasure(
                evaluation_id=evaluation.id,
                name=fake.text(256),
                primary_or_secondary=random.choice(choices.OutcomeType.values),
                direct_or_surrogate=random.choice(choices.OutcomeMeasure.values),
                measure_type=random.choice(choices.MeasureType.values),
                measure_type_other=fake.text(256),
                description=fake.text(),
                collection_process=fake.text(),
                timepoint=fake.text(),
                minimum_difference=fake.text(),
                relevance=fake.text(),
            )
        )
    models.OutcomeMeasure.objects.bulk_create(set_outcome_measures)


def generate_other_measures(evaluation):
    num_other_measures = random.randint(0, 4)
    set_other_measures = set()
    for i in range(num_other_measures):
        set_other_measures.add(
            models.OtherMeasure(
                evaluation_id=evaluation.id,
                name=fake.text(256),
                measure_type=random.choice(choices.MeasureType.values),
                measure_type_other=fake.text(256),
                description=fake.text(),
                collection_process=fake.text(),
            )
        )
    models.OtherMeasure.objects.bulk_create(set_other_measures)


def generate_processes_and_standards(evaluation):
    num_processes_and_standards = random.randint(0, 4)
    set_processes_and_standards = set()
    for i in range(num_processes_and_standards):
        set_processes_and_standards.add(
            models.ProcessStandard(
                evaluation_id=evaluation.id,
                name=fake.text(),
                conformity=random.choice(choices.FullNoPartial.values),
                description=fake.text(),
            )
        )
    models.ProcessStandard.objects.bulk_create(set_processes_and_standards)


def generate_links(evaluation):
    num_links = random.randint(0, 4)
    set_links = set()
    for i in range(num_links):
        set_links.add(
            models.LinkOtherService(
                evaluation_id=evaluation.id,
                name_of_service=fake.text(256),
                link_or_identifier=fake.url(),
            )
        )
    models.LinkOtherService.objects.bulk_create(set_links)


def make_evaluation():
    topics = generate_topics()
    organisations = generate_organisations()
    evaluation_type = generate_evaluation_types()
    data = dict(
        title=fake.text(256),
        brief_description=fake.text(),
        topics=topics,
        organisations=organisations,
        visibility=random.choice(choices.EvaluationVisibility.values),
        doi=fake.text(64),
        page_statuses=get_default_page_statuses(),
        issue_description=fake.text(),
        those_experiencing_issue=fake.text(),
        why_improvements_matter=fake.text(),
        who_improvements_matter_to=fake.text(),
        current_practice=fake.text(),
        issue_relevance=fake.text(),
        evaluation_type=evaluation_type,
        evaluation_type_other=fake.text(256),
        studied_population=fake.text(),
        eligibility_criteria=fake.text(),
        sample_size=fake.pyint(),
        sample_size_units=fake.text(5),
        sample_size_details=fake.text(),
        process_for_recruitment=fake.sentence(),
        recruitment_schedule=fake.sentence(),
        ethics_committee_approval=make_random_yes_no(),
        ethics_committee_details=fake.text(),
        ethical_state_given_existing_evidence_base=fake.text(),
        risks_to_participants=fake.text(),
        risks_to_study_team=fake.text(),
        participant_involvement=fake.text(),
        participant_information=fake.text(),
        participant_consent=fake.text(),
        participant_payment=fake.text(),
        confidentiality_and_personal_data=fake.text(),
        breaking_confidentiality=fake.text(),
        other_ethical_information=fake.text(),
        impact_design_name=random.choices(choices.ImpactEvalDesign.values),
        impact_design_name_other=fake.text(256),
        impact_design_justification=fake.text(),
        impact_design_description=fake.text(),
        impact_design_features=fake.text(),
        impact_design_equity=fake.text(),
        impact_design_assumptions=fake.text(),
        impact_design_approach_limitations=fake.text(),
        impact_framework=random.choice(choices.ImpactFramework.values),
        impact_framework_other=fake.text(256),
        impact_basis=random.choice(choices.ImpactAnalysisBasis.values),
        impact_basis_other=fake.text(256),
        impact_analysis_set=fake.text(),
        impact_effect_measure_type=random.choice(choices.ImpactMeasureType.values),
        impact_primary_effect_size_measure=fake.text(),
        impact_effect_measure_interval=random.choice(choices.ImpactMeasureInterval.values),
        impact_effect_measure_interval_other=fake.text(256),
        impact_primary_effect_size_desc=fake.text(),
        impact_interpretation_type=random.choice(choices.ImpactEvalInterpretation.values),
        impact_interpretation_type_other=fake.text(256),
        impact_sensitivity_analysis=fake.text(),
        impact_subgroup_analysis=fake.text(),
        impact_missing_data_handling=fake.text(),
        impact_fidelity=random.choice(choices.YesNo.values),
        impact_description_planned_analysis=fake.text(),
        economic_type=random.choice(choices.EconomicEvaluationType.values),
        perspective_costs=fake.text(),
        perspective_benefits=fake.text(),
        monetisation_approaches=fake.text(),
        economic_design_details=fake.text(),
        economic_analysis_description=fake.text(),
        other_design_type=fake.text(),
        other_design_details=fake.text(),
        other_analysis_description=fake.text(),
        impact_comparison=fake.text(),
        impact_outcome=fake.text(),
        impact_interpretation=random.choice(choices.ImpactEvalInterpretation.values),
        impact_point_estimate_diff=fake.text(),
        impact_lower_uncertainty=fake.text(),
        impact_upper_uncertainty=fake.text(),
        impact_summary_findings=fake.text(),
        impact_findings=fake.text(),
        process_summary_findings=fake.text(),
        process_findings=fake.text(),
        economic_summary_findings=fake.text(),
        economic_findings=fake.text(),
        other_summary_findings=fake.text(),
        other_findings=fake.text(),
        # TODO - add other fields
    )
    return data


def add_evals_to_users(user, allow_empty=True):
    num_evals = random.randint(0 if allow_empty is True else 1, 3)
    for j in range(num_evals):
        evaluation_data = make_evaluation()
        evaluation = models.Evaluation.objects.create(**evaluation_data)
        generate_costs(evaluation)
        generate_documents(evaluation)
        generate_dates(evaluation)
        generate_interventions(evaluation)
        generate_outcome_measures(evaluation)
        generate_other_measures(evaluation)
        generate_processes_and_standards(evaluation)
        generate_links(evaluation)
        evaluation.users.set([user])
        evaluation.save()
        # TODO - add other models to evaluation


def add_users(number):
    for i in range(number):
        user_data = make_fake_user()
        while models.User.objects.filter(email=user_data["email"]).exists():
            user_data = make_fake_user()
        user = models.User(**user_data)
        user.set_password("P455W0rd")
        user.save()
        add_evals_to_users(user)
        yield user
