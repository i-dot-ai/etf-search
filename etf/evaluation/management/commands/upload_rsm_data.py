import csv
import pathlib

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand

from etf.evaluation import choices
from etf.evaluation.pages import get_default_page_statuses

DATA_DIR = settings.BASE_DIR / "temp-data"
CHUNK_SIZE = 16 * 1024


# Need maps for CSV headers to model property names

generic_headers = {
    "Evaluation title": "title",  # evaluation title
    "Short title for evaluation": "short_title",  # short title
    "Evaluation summary": "brief_description",  # Description
    "Issue to be addressed": "issue_description",  # Issue description
    "Who is expecting the issue": "those_experiencing_issue",  # those experiencing the issue
    "Why the issue is important / why are improvements needed": "why_improvements_matter",  # why improvements matter
    "Who does it matter to": "who_improvements_matter_to",  # who improvements matter to
    "What difference the intervention intends to make": "issue_relevance",  # Issue relevance
    "Studied population including location(s)": "studied_population",  # Studied population
    "Eligibility criteria": "eligibility_criteria",  # Eligibility criteria
    "Total number of people (or other unit) included in the evaluation": "sample_size",  # Sample size
    "Type of unit": "sample_size_units",  # Sample size units
    "Referral / recruitment route": "process_for_recruitment",  # Process for recruitment
    "Referral / recruitment schedule": "recruitment_schedule",  # Recruitment schedule
    "Impact - Design": "impact_design_name",  # Impact evaluation design
    "Impact - Justification for design": "impact_design_justification",  # Impact design justification
    "Impact - Features to reflect real-world implementation": "impact_design_features",  # Impact design features
    "Impact - Description": "impact_design_description",  # Impact design description
    "Impact - Equity": "impact_design_equity",  # Impact design equity
    "Impact - Assumptions": "impact_design_assumptions",  # Impact design assumptions
    "Impact - Limitations of approach": "impact_design_approach_limitations",  # Impact design approach limitations
    "Economic - Costs included": "perspective_costs",  # Perspective: costs
    "Economic - Benefits included": "perspective_benefits",  # Perspective: benefits
    "Economic - Monetisation approach": "monetisation_approaches",  # Economic evaluation monetisation approaches
    "Economic - Evaluation design": "economic_design_details",  # Economic evaluation design details,
    "Other - Evaluation design": "other_design_type",  # Design type
    "Other - Summary of methods": "other_design_details",  # Design details
    # "Process - Description of analysis",  # Description of planned analysis
    "Impact - Analysis framework": "impact_framework",  # Impact analysis Framework
    "Impact - Analysis basis": "impact_basis",  # Analysis basis
    "Impact - Analysis set": "impact_analysis_set",  # Analysis set
    "Impact - Primary effect size measure type": "impact_effect_measure_type",  # Primary effect size measure type
    "Impact - Primary effect size measure": "impact_primary_effect_size_measure",  # Primary effect size measure
    "Impact - Primary effect size measure interval": "impact_effect_measure_interval",  # Primary effect size measure interval
    "Impact - Primary effect size measure description": "impact_primary_effect_size_desc",  # Primary effect size measure description
    "Impact - Interpretation type": "impact_interpretation_type",  # Interpretation type
    "Impact - Sensitivity analysis": "impact_sensitivity_analysis",  # Sensitivity analysis
    "Impact - Subgroup analysis": "impact_subgroup_analysis",  # Subgroup analysis
    "Impact - Missing data handling": "impact_missing_data_handling",  # Missing data handling
    "Impact - Fidelity of report": "impact_fidelity",  # Fidelity reporting
    "Impact - Description of analysis": "impact_description_planned_analysis",  # Description of planned analysis
    "Economic - Description of analysis": "economic_analysis_description",  # Description of planned analysis
    "Other - Description of analysis": "other_analysis_description",  # Description of planned analysis
    # "Process - Summary of findings": "",  # Summary findings
    # "Process - Findings",  # Findings
    "Economic - Summary of findings": "economic_summary_findings",  # Summary findings
    "Economic - Findings": "economic_findings",  # Findings
    "Other - Summary of findings": "other_summary_findings",  # Summary findings
    "Other - Findings": "other_findings",  # Findings
    "Ethics committee approval": "ethics_committee_approval",  # Ethics committee approval
    "Ethics committee details": "ethics_committee_details",  # Ethics committee details
    "Ethical state of study given existing evidence base": "ethical_state_given_existing_evidence_base",  # Ethical state of study given existing evidence base
    "Risks to participants": "risks_to_participants",  # Risks to participants
    "Risks to study team": "risks_to_study_team",  # Risks to study team
    "Participant involvement": "participant_involvement",  # Participant involvement
    "Participant consent (if no, why not)": "participant_consent",  # Participant consent
    "Participant information": "participant_information",  # Participant information
    "Participant payment (if yes, please elaborate)": "participant_payment",  # Participant payment
    "Confidentiality and personal data": "confidentiality_and_personal_data",  # Confidentiality and personal data
    "Breaking confidentiality": "breaking_confidentiality",  # Breaking confidentiality
    "Other ethical information": "other_ethical_information",  # Other ethical information
}

evaluation_type_headers = (
    "Process",  # Process evaluation
    "Impact",  # Impact evaluation
    "Economic",  # Economic evaluation
    "Other evaluation type (please state)",  # Other evaluation
)

organisations_headers = (
    "Government departments",  # Organisation
)

# Outcome measure
outcome_measure_headers = {
    "Outcome title": "name",  # Outcome name
    "Primary or secondary outcome": "primary_or_secondary",  # Primary or secondary
    "Direct or surrogate": "direct_or_surrogate",  # Direct or surrogate
    "Measure type": "measure_type",  # Measure type
    "Description of measure": "description",  # Description of measure
    "Collection procedures": "collection_process",  # Collection process
    "Minimum practically important difference": "minimum_difference",  # Minimum practically important difference
    "Relevance of outcome": "relevance",  # Relevance of outcome
}

# Other measure
other_measure_headers = {
    "Other outcomes - Outcome name": "name",  # Measurement name
    "Other outcomes - Outcome measure type": "measure_type",  # Measure type
    "Other outcomes - Description of measure": "description",  # Description of measurement
    "Other outcomes - Collection procedures and timing": "collection_process",  # Collection procedures and timing
}

# Grants
grant_headers = {}

# Links
links_headers = {
    "Links to associated docments": "link_or_identifier",
}

# Interventions
intervention_headers = {
    "Intervention name": "name",  # Intervention name
    "Intervention brief description": "brief_description",  # Intervention brief description
    "Intervention rationale": "rationale",  # Intervention rationale
    "Materials used": "materials_used",  # Intervention materials used
    "Procedures used": "procedures",  # Intervention procedures
    "Who delivered the intervention": "provider_description",  # Intervention provider description
    "How was the intervention delivered": "modes_of_delivery",  # Intervention modes of delivery
    "Where was the intervention delivered": "location",  # Intervention location
    "How often the intervention was delivered": "frequency_of_delivery",  # Intervention frequency of delivery
    "Tailoring": "tailoring",  # Intervention tailoring
    "How well it was delivered (fidelity)": "fidelity",  # Intervention fidelity
    "Resource requirements": "resource_requirements",  # Intervention resource requirements
    "Geographical information": "geographical_information",  # Intervention geographical information
}

# Event dates
event_date_headers = {}

# Evaluation costs
evaluation_cost_headers = {
    "Evaluation cost (£)": "item_cost",
}

# Processes and standards
processes_and_standards_headers = {
    "Name of standard or process": "name",  # Name of standard of process
    "Conformity": "conformity",  # Conformity of standard or process
    "Process and standards - Description": "description",  # Description of standard or process
}

unique_field_headers = (
    "Intervention start date (Month)",  # Intervention - when ?
    "Intervention start date (Year)",  # Intervention - when ?
    "Intervention end date (Month)",  # Intervention - when ?
    "Intervention end date (Year)",  # Intervention - when ?
    "Time point of interest (Month)",  # Timepoint(s) of interest
    "Time point of interest (Year)",  # Timepoint(s) of interest
    "aspect_name",  # Used by two models, with different option lists in each
)

single_choice_fields = {
    "ethics_committee_approval": choices.YesNo,
    "impact_framework": choices.ImpactFramework,
    "impact_basis": choices.ImpactAnalysisBasis,
    "impact_effect_measure_type": choices.ImpactMeasureType,
    "impact_effect_measure_interval": choices.ImpactMeasureInterval,
    "impact_interpretation_type": choices.ImpactInterpretationType,
    "impact_fidelity": choices.YesNo,
    "economic_type": choices.EconomicEvaluationType,
    "impact_interpretation": choices.ImpactEvalInterpretation,
    "primary_or_secondary": choices.OutcomeType,
    "direct_or_surrogate": choices.OutcomeMeasure,
    "measure_type": choices.MeasureType,  # For both Other and Outcome measures
    "conformity": choices.FullNoPartial,
    "event_date_name": choices.EventDateOption,
    "event_date_type": choices.EventDateType,
    "method_name": choices.ProcessEvaluationMethods,
}

multiple_choice_fields = {
    "impact_design_name": choices.ImpactEvalDesign,
    "document_types": choices.DocumentType,
    "aspects_measured": choices.ProcessEvaluationAspects,
}

default_fields = {
    "visibility": "DRAFT",
    "page_statuses": get_default_page_statuses()
}

derived_fields = (
    "issue_description_option",
    "ethics_option",
    "grants_option",
)


# TODO: List contains all relevant headers
all_headers = (
    list(key for key in generic_headers.keys())
    + list(key for key in outcome_measure_headers.keys())
    + list(key for key in other_measure_headers.keys())
    + list(key for key in grant_headers.keys())
    + list(key for key in links_headers.keys())
    + list(key for key in intervention_headers.keys())
    + list(key for key in event_date_headers.keys())
    + list(key for key in evaluation_cost_headers.keys())
    + list(key for key in processes_and_standards_headers.keys())
)


class Command(BaseCommand):
    help = "Populate Evaluation Registry with data from RSM"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--url", type=str, help="URL of data to upload")

    def handle(self, *args, **kwargs):
        url = kwargs["url"]
        import_and_upload_evaluations(url)


def save_url_to_data_dir(url):
    filename = pathlib.Path(url).stem
    filepath = DATA_DIR / "".join((filename, pathlib.Path(url).suffix))
    if not filepath.exists():
        print(f"Downloading to: {filepath}")  # noqa: T201
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("wb") as f:
            with httpx.stream("GET", url) as response:
                for chunk in response.iter_bytes(CHUNK_SIZE):
                    f.write(chunk)
    else:
        print(f"Skipping download: {filepath} already exists")  # noqa: T201
    return filepath


def get_sheet_headers(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
    for header in headers:
        print(header)
    return headers


def get_evaluation_ids(data, headers):
    unique_ids = set()
    column_index = headers.index("Evaluation ID")
    for row in data:
        id_value = row[column_index]
        if id_value:
            unique_ids.add(id_value)
    return sorted(unique_ids)


def get_data_rows(filename):
    data = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        _ = next(reader)
        for row in reader:
            data.append(row)
        return data


def get_evaluation_rows_for_id(unique_id, rows, headers):
    column_index = headers.index("Evaluation ID")
    matching_rows = [row for row in rows if row[column_index] == unique_id]
    return matching_rows


def transform_and_create_from_rows(rows):
    # print(rows)
    return rows


def import_and_upload_evaluations(url):
    filename = save_url_to_data_dir(url)
    headers = get_sheet_headers(filename)
    rows = get_data_rows(filename)
    unique_ids = get_evaluation_ids(rows, headers)
    unique_id = unique_ids[0]
    rows_for_id = get_evaluation_rows_for_id(unique_id, rows, headers)
    transform_and_create_from_rows([rows_for_id[0]])
    # for unique_id in unique_ids:
    #     rows_for_id = get_evaluation_rows_for_id(unique_id, rows, headers)
    #     transform_and_create_from_rows(rows_for_id)
