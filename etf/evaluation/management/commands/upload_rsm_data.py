import csv
import pathlib

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand

from etf.evaluation import choices, enums, models

DATA_DIR = settings.BASE_DIR / "temp-data"
CHUNK_SIZE = 16 * 1024


# Ensure all data matching maps are in lower case for lower matches

disallowed_row_values = (
    "information not identified within the report",
    "information not identified in the report",
    "not identified",
    "information not easily identified within the report",
    "other (please specify)",
    "not announced",
    "n/a",
    "na",
    "no information easily identified within the report",
    "information not included in the report",
    "information not specified within the report",
    "information not specifed in report",
    "information not specified in the report",
    "not applicable",
    "not applicabe",
    "no information on outcomes easily identified within the report",
    "information notidentified within the report",
    "no information on outcomes easily identified within the report" "information no identified within the report",
    "no outcomes identified within the report",
    "not found",
    "information no identified within the report",
    "information not identfied within the report",
    "information specified in a separate report",
    "missing - needs to be added",
    "0",
    "1",
    "Not applicablle",
    "no methodology identified within the report",
    "not applicablle",
)

positive_row_values = (
    "y",
    "yes",
    "true",
)

negative_row_values = (
    "n",
    "no",
    "false",
)


class AlternateChoice:
    def __init__(self, label, name):
        self.label = label
        self.name = name


yes_no_choices = (
    AlternateChoice(label="y", name=choices.YesNo.YES),
    AlternateChoice(label="y (aa)", name=choices.YesNo.YES),
    AlternateChoice(label="yes", name=choices.YesNo.YES),
    AlternateChoice(label="n", name=choices.YesNo.NO),
    AlternateChoice(label="no", name=choices.YesNo.NO),
)

impact_design_name_choices = (
    AlternateChoice(label="surveys and polling", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="individual interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS),
    AlternateChoice(
        label="output or performance monitoring", name=choices.ImpactEvalDesign.OUTPUT_OR_PERFORMANCE_MONITORING
    ),
    AlternateChoice(label="Randomised Controlled Trial (RCT)", name=choices.ImpactEvalDesign.RCT),
    AlternateChoice(label="Interviews and group sessions", name=choices.ImpactEvalDesign.FOCUS_GROUPS),
    AlternateChoice(label="Surveys (ECTs)", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(
        label="Output or performance monitoring", name=choices.ImpactEvalDesign.OUTPUT_OR_PERFORMANCE_MONITORING
    ),
    AlternateChoice(label="Cluster randomised RCT", name=choices.ImpactEvalDesign.CLUSTER_RCT),
    AlternateChoice(
        label="Surveys, focus groups and interviews conducted", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING
    ),
    AlternateChoice(label="Propensity Score Matching", name=choices.ImpactEvalDesign.PROPENSITY_SCORE_MATCHING),
    AlternateChoice(
        label="Focus groups or group interviews alongwith individual interviews & case studies",
        name=choices.ImpactEvalDesign.FOCUS_GROUPS,
    ),
    AlternateChoice(label="Difference in Difference", name=choices.ImpactEvalDesign.DIFF_IN_DIFF),
    AlternateChoice(
        label="Output or performance review", name=choices.ImpactEvalDesign.OUTPUT_OR_PERFORMANCE_MONITORING
    ),
    AlternateChoice(label="Survey and polling", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="Individual interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS),
    AlternateChoice(label="Case studies", name=choices.ImpactEvalDesign.CASE_STUDIES),
    AlternateChoice(label="Survey respondents (landlords)", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="Simulation model developed", name=choices.ImpactEvalDesign.SIMULATION_MODELLING),
    AlternateChoice(label="Focus groups or group interviews", name=choices.ImpactEvalDesign.FOCUS_GROUPS),
    AlternateChoice(label="Outcome letter review", name=choices.ImpactEvalDesign.OUTCOME_HARVESTING),
    AlternateChoice(label="Semi structured qualitative interviews", name=choices.ImpactEvalDesign.QCA),
    AlternateChoice(
        label="Other (Qualitative research)", name=choices.ImpactEvalDesign.QUALITATIVE_OBSERVATIONAL_STUDIES
    ),
    AlternateChoice(
        label="Mix of methods including surveys and group interviews", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING
    ),
    AlternateChoice(
        label="Telephone interviews (housing advisers)", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS
    ),
    AlternateChoice(label="Individual interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS),
    AlternateChoice(label="Focus groups, interviews, and surveys", name=choices.ImpactEvalDesign.FOCUS_GROUPS),
    AlternateChoice(
        label="Review of data from Adult Tobacco Policy Survey", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING
    ),
    AlternateChoice(label="Consultative/deliberative methods", name=choices.ImpactEvalDesign.CONSULTATIVE_METHODS),
    AlternateChoice(label="Surveys (senior leaders)", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="Randomised Controlled Trial", name=choices.ImpactEvalDesign.RCT),
    AlternateChoice(label="Synthetic Control Methods", name=choices.ImpactEvalDesign.SYNTHETIC_CONTROL_METHODS),
    AlternateChoice(label="interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS),
    AlternateChoice(
        label="qualitative depth interviews and focus groups",
        name=choices.ImpactEvalDesign.QUALITATIVE_OBSERVATIONAL_STUDIES,
    ),
    AlternateChoice(label="Case Studies", name=choices.ImpactEvalDesign.CASE_STUDIES),
    AlternateChoice(label="Case studies and interviews", name=choices.ImpactEvalDesign.CASE_STUDIES),
    AlternateChoice(label="Simulation modelling", name=choices.ImpactEvalDesign.SIMULATION_MODELLING),
    AlternateChoice(label="Focus group", name=choices.ImpactEvalDesign.FOCUS_GROUPS),
    AlternateChoice(label="Interviews (landlords)", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS),
    AlternateChoice(label="Process Tracing", name=choices.ImpactEvalDesign.PROCESS_TRACING),
    AlternateChoice(label="Interview", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS),
    AlternateChoice(
        label="regression adjusted Difference-in-Difference (DiD)", name=choices.ImpactEvalDesign.DIFF_IN_DIFF
    ),
    AlternateChoice(label="Survyes and case study", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="Participant Survey", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="focus groups", name=choices.ImpactEvalDesign.FOCUS_GROUPS),
    AlternateChoice(label="INTERVIEW", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS),
    AlternateChoice(label="Surveys and polling", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="Surveys and interviews", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="Focus groups (housing advisers)", name=choices.ImpactEvalDesign.FOCUS_GROUPS),
    AlternateChoice(label="Forcus group", name=choices.ImpactEvalDesign.FOCUS_GROUPS),
    AlternateChoice(label="Contribution Tracing", name=choices.ImpactEvalDesign.CONTRIBUTION_TRACING),
    AlternateChoice(label="Surveys", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING),
    AlternateChoice(label="Outcome harvesting", name=choices.ImpactEvalDesign.OUTCOME_HARVESTING),
    AlternateChoice(
        label="Performance or output monitoring", name=choices.ImpactEvalDesign.OUTPUT_OR_PERFORMANCE_MONITORING
    ),
    AlternateChoice(
        label="Individual interviews along with surveys and review of monitoring data to carry out quantitative modelling approach",
        name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS,
    ),
    AlternateChoice(
        label="Simulation modelling: Asset Liability Modelling (ALM)",
        name=choices.ImpactEvalDesign.SIMULATION_MODELLING,
    ),
    AlternateChoice(label="Other (RCT - Quasi-Experimentl approaches)", name=choices.ImpactEvalDesign.RCT),
)


evaluation_headers = {
    "Evaluation title": {"field_name": "title", "resolution_method": "single", "data_type": "str"},
    "Short title for evaluation": {"field_name": "short_title", "resolution_method": "single", "data_type": "str"},
    "Evaluation summary": {"field_name": "brief_description", "resolution_method": "combine", "data_type": "str"},
    "Issue to be addressed": {"field_name": "issue_description", "resolution_method": "combine", "data_type": "str"},
    "Who is experiencing the issue": {
        "field_name": "those_experiencing_issue",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Why the issue is important / why are improvements needed": {
        "field_name": "why_improvements_matter",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Who does it matter to": {
        "field_name": "who_improvements_matter_to",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "What difference the intervention intends to make": {
        "field_name": "issue_relevance",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Studied population including location(s)": {
        "field_name": "studied_population",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Eligibility criteria": {"field_name": "eligibility_criteria", "resolution_method": "combine", "data_type": "str"},
    "Total number of people (or other unit) included in the evaluation": {
        "field_name": "sample_size",
        "resolution_method": "combine",
        "data_type": "int",
    },
    "Type of unit": {"field_name": "sample_size_units", "resolution_method": "single", "data_type": "str"},
    "Referral / recruitment route": {
        "field_name": "process_for_recruitment",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Referral / recruitment schedule": {
        "field_name": "recruitment_schedule",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Design": {
        "field_name": "impact_design_name",
        "resolution_method": "multiple_choice",
        "data_type": impact_design_name_choices,
    },
    "Impact - Justification for design": {
        "field_name": "impact_design_justification",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Features to reflect real-world implementation": {
        "field_name": "impact_design_features",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Description": {
        "field_name": "impact_design_description",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Equity": {"field_name": "impact_design_equity", "resolution_method": "combine", "data_type": "str"},
    "Impact - Assumptions": {
        "field_name": "impact_design_assumptions",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Limitations of approach": {
        "field_name": "impact_design_approach_limitations",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Economic - Costs included": {
        "field_name": "perspective_costs",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Economic - Benefits included": {
        "field_name": "perspective_benefits",
        "resolution_method": "Combine",
        "data_type": "str",
    },
    "Economic - Monetisation approach": {
        "field_name": "monetisation_approaches",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Economic - Evaluation design": {
        "field_name": "economic_design_details",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Other - Evaluation design": {
        "field_name": "other_design_type",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Other - Summary of methods": {
        "field_name": "other_design_details",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Analysis framework": {
        "field_name": "impact_framework",
        "resolution_method": "choice",
        "data_type": choices.ImpactFramework,
    },
    "Impact - Analysis basis": {
        "field_name": "impact_basis",
        "resolution_method": "choice",
        "data_type": choices.ImpactAnalysisBasis,
    },
    "Impact - Analysis set": {"field_name": "impact_analysis_set", "resolution_method": "combine", "data_type": "str"},
    "Impact - Primary effect size measure type": {
        "field_name": "impact_effect_measure_type",
        "resolution_method": "choice",
        "data_type": choices.ImpactMeasureType,
    },
    "Impact - Primary effect size measure": {
        "field_name": "impact_primary_effect_size_measure",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Primary effect size measure interval": {
        "field_name": "impact_effect_measure_interval",
        "resolution_method": "choice",
        "data_type": choices.ImpactMeasureInterval,
    },
    "Impact - Primary effect size measure description": {
        "field_name": "impact_primary_effect_size_desc",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Interpretation type": {
        "field_name": "impact_interpretation_type",
        "resolution_method": "choice",
        "data_type": choices.ImpactInterpretationType,
    },
    "Impact - Sensitivity analysis": {
        "field_name": "impact_sensitivity_analysis",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Subgroup analysis": {
        "field_name": "impact_subgroup_analysis",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Missing data handling": {
        "field_name": "impact_missing_data_handling",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Impact - Fidelity of report": {
        "field_name": "impact_fidelity",
        "resolution_method": "choice",
        "data_type": yes_no_choices,
    },
    "Impact - Description of analysis": {
        "field_name": "impact_description_planned_analysis",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Economic - Description of analysis": {
        "field_name": "economic_analysis_description",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Other - Description of analysis": {
        "field_name": "other_analysis_description",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Economic - Summary of findings": {
        "field_name": "economic_summary_findings",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Economic - Findings": {"field_name": "economic_findings", "resolution_method": "combine", "data_type": "str"},
    "Other - Summary of findings": {
        "field_name": "other_summary_findings",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Other - Findings": {"field_name": "other_findings", "resolution_method": "combine", "data_type": "str"},
    "Ethics committee approval": {
        "field_name": "ethics_committee_approval",
        "resolution_method": "choice",
        "data_type": yes_no_choices,
    },
    "Ethics committee details": {
        "field_name": "ethics_committee_details",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Ethical state of study given existing evidence base": {
        "field_name": "ethical_state_given_existing_evidence_base",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Risks to participants": {
        "field_name": "risks_to_participants",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Risks to study team": {"field_name": "risks_to_study_team", "resolution_method": "combine", "data_type": "str"},
    "Participant involvement": {
        "field_name": "participant_involvement",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Participant consent (if no, why not)": {
        "field_name": "participant_consent",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Participant information": {
        "field_name": "participant_information",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Participant payment (if yes, please elaborate)": {
        "field_name": "participant_payment",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Confidentiality and personal data": {
        "field_name": "confidentiality_and_personal_data",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Breaking confidentiality": {
        "field_name": "breaking_confidentiality",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Other ethical information": {
        "field_name": "other_ethical_information",
        "resolution_method": "combine",
        "data_type": "str",
    },
}

# Organisation
organisations_headers = {
    "Government departments": {
        "field_name": "organisations",
        "resolution_method": "multiple_choice",
        "data_type": enums.Organisation.choices,
    }
}

# Outcome measure
outcome_measure_headers = {
    "Outcome title": {
        "field_name": "name",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Primary or secondary outcome": {
        "field_name": "primary_or_secondary",
        "resolution_method": "choice",
        "data_type": choices.OutcomeType,
    },
    "Direct or surrogate": {
        "field_name": "direct_or_surrogate",
        "resolution_method": "choice",
        "data_type": choices.OutcomeMeasure,
    },
    "Measure type": {"field_name": "measure_type", "resolution_method": "choice", "data_type": choices.MeasureType},
    "Description of measure": {
        "field_name": "description",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Collection procedures": {
        "field_name": "collection_process",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Minimum practically important difference": {
        "field_name": "minimum_difference",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Relevance of outcome": {
        "field_name": "relevance",
        "resolution_method": "single",
        "data_type": "str",
    },
}

# Other measure
other_measure_headers = {
    "Other outcomes - Outcome name": {
        "field_name": "name",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Other outcomes - Outcome measure type": {
        "field_name": "measure_type",
        "resolution_method": "choice",
        "data_type": choices.MeasureType,
    },
    "Other outcomes - Description of measure": {
        "field_name": "description",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Other outcomes - Collection procedures and timing": {
        "field_name": "collection_process",
        "resolution_method": "single",
        "data_type": "str",
    },
}

# Grants
grant_headers = {}

# Links
links_headers = {
    "Links to associated docments": {
        "field_name": "link_or_identifier",
        "resolution_method": "single",
        "data_type": "str",
    },
}

# Interventions
intervention_headers = {
    "Intervention name": {
        "field_name": "name",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Intervention brief description": {
        "field_name": "brief_description",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Intervention rationale": {
        "field_name": "rationale",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Materials used": {
        "field_name": "materials_used",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Procedures used": {
        "field_name": "procedures",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Who delivered the intervention": {
        "field_name": "provider_description",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "How was the intervention delivered": {
        "field_name": "modes_of_delivery",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Where was the intervention delivered": {
        "field_name": "location",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "How often the intervention was delivered": {
        "field_name": "frequency_of_delivery",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Tailoring": {
        "field_name": "tailoring",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "How well it was delivered (fidelity)": {
        "field_name": "fidelity",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Resource requirements": {
        "field_name": "resource_requirements",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Geographical information": {
        "field_name": "geographical_information",
        "resolution_method": "combine",
        "data_type": "str",
    },
}

# Event dates
event_date_headers = {}

# Evaluation costs
evaluation_cost_headers = {
    "Evaluation cost (£)": {
        "field_name": "item_cost",
        "resolution_method": "combine",
        "data_type": "str",
    },
}

# Processes and standards
processes_and_standards_headers = {
    "Name of standard or process": "name",  # Name of standard of process
    "Conformity": {
        "field_name": "conformity",
        "resolution_method": "choice",
        "data_type": choices.FullNoPartial,
    },
    "Process and standards - Description": "description",  # Description of standard or process
}

unique_field_headers = (
    "Intervention start date (Month)",  # Intervention - when ?
    "Intervention start date (Year)",  # Intervention - when ?
    "Intervention end date (Month)",  # Intervention - when ?
    "Intervention end date (Year)",  # Intervention - when ?
    "Time point of intesest (Month)",  # Timepoint(s) of interest, intended typo
    "Time point of intesest (Year)",  # Timepoint(s) of interest, intended typo
)

derived_fields = {
    "issue_description_option": "Issue to be addressed",  # Evaluation optional page
    "ethics_option": "Ethics committee approval",  # Evaluation optional page
    # "grants_option", Evaluation optional page, not present in CSV yet
    "process_evaluation": "Process",  # Evaluation type option
    "impact_evaluation": "Impact",  # Evaluation type option
    "economic_evaluation": "Economic",  # Evaluation type option
    "other_evaluation": "Other evaluation type (please state)",  # Evaluation type option
    "sample_size_details": "Total number of people (or other unit) included in the evaluation",  # Taken from sample_size column and all text goes here instead
}


# TODO: List contains all relevant headers
all_headers = (
    list(key for key in evaluation_headers.keys())
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
        headers = [header for header in headers if header != ""]
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


def get_values_from_rows_for_header(rows, header, headers):
    values_of_header_rows = [row[headers.index(header)] for row in rows]

    # Removed empty, unwanted and duplicate values
    allowed_values = []
    for value in values_of_header_rows:
        contains_disallowed = False
        for disallowed in disallowed_row_values:
            if disallowed in value.lower() or value.strip() == "" or value is None:
                contains_disallowed = True
                break
        if not contains_disallowed:
            allowed_values.append(value)
    return list(set(allowed_values))


def handle_simple_field(model, header_entry, values_of_header_rows):
    if values_of_header_rows:
        if header_entry["resolution_method"] == "combine":
            if header_entry["data_type"] == "str":
                value = ". ".join(s.strip().rstrip(".") for s in values_of_header_rows) + "."
            else:
                value = sum(float(v) for v in values_of_header_rows if v.isdigit())
        elif header_entry["resolution_method"] == "single":
            if header_entry["data_type"] == "str":
                value = max(set(values_of_header_rows), key=values_of_header_rows.count)
            else:
                all_float_values = [float(v) for v in values_of_header_rows if v.isdigit()]
                value = max(all_float_values) if all_float_values else 0
        else:
            value = "" if header_entry["data_type"] == "str" else 0
    else:
        value = "" if header_entry["data_type"] == "str" else 0
    setattr(model, header_entry["field_name"], value)
    model.save()


def handle_derived_evaluation_fields(evaluation, rows, headers):
    issue_description_row_values = get_values_from_rows_for_header(
        rows, derived_fields["issue_description_option"], headers
    )
    if issue_description_row_values:
        setattr(evaluation, "issue_description_option", "YES")
    else:
        setattr(evaluation, "issue_description_option", "NO")
        evaluation.save()

    ethics_row_values = get_values_from_rows_for_header(rows, derived_fields["ethics_option"], headers)
    if ethics_row_values:
        setattr(evaluation, "ethics_option", "YES")
    else:
        setattr(evaluation, "ethics_option", "NO")
        evaluation.save()

    # "grants_option", Evaluation optional page, not there in CSV
    setattr(evaluation, "grants_option", "NO")
    evaluation.save()

    evaluation_types = []
    process_evaluation_row_values = get_values_from_rows_for_header(rows, derived_fields["process_evaluation"], headers)
    process_evaluation_row_values_yes = sum(
        1 for row_value in process_evaluation_row_values if row_value.lower() in positive_row_values
    )
    process_evaluation_row_values_no = sum(
        1 for row_value in process_evaluation_row_values if row_value.lower() in negative_row_values
    )
    if process_evaluation_row_values_no > process_evaluation_row_values_yes:
        evaluation_types.append(choices.EvaluationTypeOptions.PROCESS.value)

    impact_evaluation_row_values = get_values_from_rows_for_header(rows, derived_fields["impact_evaluation"], headers)
    impact_evaluation_row_values_yes = sum(
        1 for row_value in impact_evaluation_row_values if row_value.lower() in positive_row_values
    )
    impact_evaluation_row_values_no = sum(
        1 for row_value in impact_evaluation_row_values if row_value.lower() in negative_row_values
    )
    if impact_evaluation_row_values_no > impact_evaluation_row_values_yes:
        evaluation_types.append(choices.EvaluationTypeOptions.IMPACT.value)

    economic_evaluation_row_values = get_values_from_rows_for_header(
        rows, derived_fields["economic_evaluation"], headers
    )
    economic_evaluation_row_values_yes = sum(
        1 for row_value in economic_evaluation_row_values if row_value.lower() in positive_row_values
    )
    economic_evaluation_row_values_no = sum(
        1 for row_value in economic_evaluation_row_values if row_value.lower() in negative_row_values
    )
    if economic_evaluation_row_values_no > economic_evaluation_row_values_yes:
        evaluation_types.append(choices.EvaluationTypeOptions.ECONOMIC.value)

    other_evaluation_row_values = get_values_from_rows_for_header(rows, derived_fields["other_evaluation"], headers)
    other_evaluation_row_values_yes = sum(
        1 for row_value in other_evaluation_row_values if row_value.lower() in positive_row_values
    )
    other_evaluation_row_values_no = sum(
        1 for row_value in other_evaluation_row_values if row_value.lower() in negative_row_values
    )
    other_evaluation_row_values = [
        row_value
        for row_value in other_evaluation_row_values
        if (row_value.lower() not in positive_row_values and row_value.lower() not in negative_row_values)
    ]
    if other_evaluation_row_values_yes > other_evaluation_row_values_no:
        evaluation_types.append(choices.EvaluationTypeOptions.OTHER.value)
        if other_evaluation_row_values:
            setattr(evaluation, "evaluation_type_other", other_evaluation_row_values)
        else:
            setattr(evaluation, "evaluation_type_other", "No information provided.")
    setattr(evaluation, "evaluation_type", evaluation_types)
    evaluation.save()

    sample_size_values = get_values_from_rows_for_header(rows, derived_fields["sample_size_details"], headers)
    sample_size_values_text = [sample_size for sample_size in sample_size_values if not sample_size.isdigit()]
    sample_size_details = ". ".join(s.strip().rstrip(".") for s in sample_size_values_text) + "."
    setattr(evaluation, "sample_size_details", sample_size_details)
    evaluation.save()


def handle_single_choice_field(model, header_entry, values_of_header_rows):
    if values_of_header_rows:
        most_chosen_choice = max(set(values_of_header_rows), key=values_of_header_rows.count)
        most_chosen_choice = most_chosen_choice.rstrip(".")
        item_choices = header_entry["data_type"]
        selected_choice = [choice.name for choice in item_choices if choice.label.lower() == most_chosen_choice.lower()]
        if selected_choice:
            value = selected_choice[0]
            setattr(model, header_entry["field_name"], value)
        else:
            value = "OTHER"
            setattr(model, header_entry["field_name"], value)
            other_value = ". ".join(s.strip().rstrip(".") for s in values_of_header_rows) + "."
            setattr(model, f"{header_entry['field_name']}_other", other_value)
        model.save()


def handle_multiple_choice_field(model, header_entry, values_of_header_rows):
    if values_of_header_rows:
        item_choices = header_entry["data_type"]
        lower_values_of_header_rows = [row_value.lower().strip().rstrip(".") for row_value in values_of_header_rows]
        present_choices = [
            choice.label for choice in item_choices if choice.label.lower() in lower_values_of_header_rows
        ]
        not_present_choices = [
            lower_value_of_header_rows
            for lower_value_of_header_rows in lower_values_of_header_rows
            if lower_value_of_header_rows not in item_choices
        ]
        if present_choices:
            setattr(model, header_entry["field_name"], present_choices)
            model.save()
        if not_present_choices:
            if "OTHER" not in present_choices:
                present_choices.append("OTHER")
                setattr(model, header_entry["field_name"], present_choices)
            other_value = ". ".join(s.strip().rstrip(".") for s in not_present_choices) + "."
            setattr(model, f"{header_entry['field_name']}_other", other_value)
            model.save()


def transform_and_create_from_rows(rows, headers):
    evaluation = models.Evaluation.objects.create()
    evaluation.visibility = "PUBLIC"
    evaluation.save()

    # Check header type from dict
    # Functions for each type
    # Assign evaluation value based on header value, type and resolution type (make sure remove values from disallowed values array)
    # Organisation needs to be split by ';', stripped and compared in a 'contain' query

    # Evaluation headers
    for header in headers:
        if header in evaluation_headers:
            header_entry = evaluation_headers[header]
            values_of_header_rows = get_values_from_rows_for_header(rows, header, headers)
            if header_entry["data_type"] in (
                "str",
                "int",
            ):
                handle_simple_field(evaluation, header_entry, values_of_header_rows)
            elif header_entry["resolution_method"] == "choice":
                handle_single_choice_field(evaluation, header_entry, values_of_header_rows)
            elif header_entry["resolution_method"] == "multiple_choice":
                handle_multiple_choice_field(evaluation, header_entry, values_of_header_rows)

    # Derived evaluation headers
    handle_derived_evaluation_fields(evaluation, rows, headers)

    return rows


single_choice_fields = {
    "Impact - Analysis framework": choices.ImpactFramework,  # Most don't match, going to have to match with OTHER mostly
    "Impact - Analysis basis": choices.ImpactAnalysisBasis,  # Matches exactly
    "Impact - Primary effect size measure type": choices.ImpactMeasureType,  # Only a small amount match, all others should go into "Other"
    "Impact - Primary effect size measure interval": choices.ImpactMeasureInterval,  # Some match, some don't, add extras to "Other"
    "Impact - Interpretation type": choices.ImpactInterpretationType,  # Some match, others don't so add to "other", should we add "None" to accepted values
    "Impact - Fidelity of report": choices.YesNo,  # Need a new match for yes/no, options are Y, N and Y (AA), ignore extras
    "Ethics committee approval": choices.YesNo,  # Need a new match for yes/no, options are Y, N and Y (AA), ignore extras
    "Primary or secondary outcome": choices.OutcomeType,  # Some match, ignore those that don't
    "Direct or surrogate": choices.OutcomeMeasure,  # Some match, ignore those that don't
    "Measure type": choices.MeasureType,  # Matches types for some (do lower comparison anyway) Other is implied by not matching any
    "Other outcomes - Outcome measure type": choices.MeasureType,  # Matches types for some (do lower comparison anyway) Other is implied by not matching any
    "Conformity": choices.FullNoPartial,  # Matches values (do lower comparison anyway)
}


multi_choice_fields = {
    # "topics": choices.Topic,  # Not included in CSV
    # "evaluation type": choices.EvaluationTypeOptions,  # Done with derived fields
    "Impact - Design": choices.ImpactEvalDesign,  # impact design name
    # "document types": choices.DocumentType,  # Documents not included in csv,
    # "aspect name": choices.ProcessEvaluationAspects,  # in ProcessEvaluationDesignAspectsSchema, not in CSV
    # "aspects_measured": choices.ProcessEvaluationAspects,  # in ProcessEvaluationMethodSchema, not in CSV
}


def import_and_upload_evaluations(url):
    filename = save_url_to_data_dir(url)
    headers = get_sheet_headers(filename)
    rows = get_data_rows(filename)
    # for choice_field in multi_choice_fields.keys():
    #     values = get_values_from_rows_for_header(rows, choice_field, headers)
    #     for value in values:
    #         print(value)
    #         print("\n")
    unique_ids = get_evaluation_ids(rows, headers)
    for unique_id in unique_ids[0:2]:
        rows_for_id = get_evaluation_rows_for_id(unique_id, rows, headers)
        transform_and_create_from_rows(rows_for_id, headers)
