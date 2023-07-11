"""
This is for the upload of the RSM data - to initially populate the Evaluation Registry.
In theory, should just be done the once.
"""
import math
import pathlib

import pandas as pd

from eva_reg.evaluation import choices, enums, models

DATA_DIR = pathlib.Path("eva_reg", "data")
INFO_NOT_IDENTIFIED = "Information not identified within the report"

EVALUATION_STANDARD_FIELDS_LOOKUP = {
    "title": "evaluation_information_evaluation_title",
    "brief_description": "evaluation_information_evaluation_summary",  # TODO - many of these?
    # "issue_description":
    # "those_experiencing_issue":
    # "why_improvements_matter":
    # "who_improvements_matter_to":
    # "current_practice":
    # "issue_relevance":
    # topics = models.JSONField(default=list)  # TODO - do we use these?
    # organisations = models.JSONField(default=list)  # TODO - how are we going to do orgs?
    "issue_description": "issue_issue_to_be_addressed",
    "those_experiencing_issue": "issue_who_is_experiencing_the_issue",
    "why_improvements_matter": "issue_why_the_issue_is_important__why_are_improvements_needed",
    "who_improvements_matter_to": "issue_who_does_it_matter_to",
    "current_practice": "issue_current_practice",
    "issue_relevance": "issue_what_difference_the_intervention_intends_to_make",
    # TODO - Studied population - should there be many rows? (There are in Excel)
    "studied_population": "study_population_studied_population_including_location(s)",
    "eligibility_criteria": "study_population_eligibility_criteria",
    # "sample_size": 'study_population_total_number_of_people_(or_other_unit)_included_in_the_evaluation' TODO - pos int field
    "sample_size_units": "study_population_type_of_unit",
    # "sample_size_details" TODO - no match-up
    # Participant recruitment approach
    "process_for_recruitment": "evaluation_recruitment_referral__recruitment_route",
    "recruitment_schedule": "evaluation_recruitment_referral__recruitment_schedule",
    # Ethical considerations
    # "ethics_committee_approval": "ethical_considerations_ethics_committee_approval", #TODO - choices field
    "ethics_committee_details": "ethical_considerations_ethics_committee_details",
    "ethical_state_given_existing_evidence_base": "ethical_considerations_ethical_state_of_study_given_existing_evidence_base",
    "risks_to_participants": "ethical_considerations_risks_to_participants",
    "risks_to_study_team": "ethical_considerations_risks_to_study_team",
    "participant_involvement": "ethical_considerations_participant_involvement",
    "participant_information": "ethical_considerations_participant_information",
    "participant_consent": "ethical_considerations_participant_consent_(if_no,_why_not)",
    "participant_payment": "ethical_considerations_participant_payment_(if_yes,_please_ellaborate)",
    "confidentiality_and_personal_data": "ethical_considerations_confidentiality_and_personal_data",
    "breaking_confidentiality": "ethical_considerations_breaking_confidentiality",
    "other_ethical_information": "ethical_considerations_other_ethical_information",
    # Impact evaluation design
    # "impact_design_name": "impact_evaluation_design_design" TODO - JSON field/list
    # other
    "impact_design_justification": "impact_evaluation_design_justification_for_design",
    "impact_design_description": "impact_evaluation_design_description",
    "impact_design_features": "impact_evaluation_design_features_to_reflect_real-world_implementation",
    "impact_design_equity": "impact_evaluation_design_equity",
    "impact_design_assumptions": "impact_evaluation_design_assumptions",
    "impact_design_approach_limitations": "impact_evaluation_design_limitations_of_approach",
    # TODO - most of these are choice fields
    # "impact_framework": "impact_evaluation_analysis_analysis_framework" TODO - choice field
    # "impact_framework_other"
    # "impact_basis": "impact_evaluation_analysis_analysis_basis",
    # "impact_basis_other"
    # "impact_analysis_set": "impact_evaluation_analysis_analysis_set"
    # "impact_effect_measure_type": "impact_evaluation_analysis_primary_effect_size_measure_type"
    # "impact_primary_effect_size_measure": "impact_evaluation_analysis_primary_effect_size_measure"
    # "impact_effect_measure_interval": "impact_evaluation_analysis_primary_effect_size_measure_interval"
    # "impact_primary_effect_size_desc": "impact_evaluation_analysis_primary_effect_size_measure_description"
    # "impact_interpretation_type": "impact_evaluation_analysis_interpretation_type"
    # impact_interpretation_type_other
    # "impact_sensitivity_analysis": "impact_evaluation_analysis_sensitivity_analysis"
    # "impact_subgroup_analysis": "impact_evaluation_analysis_subgroup_analysis"
    # "impact_missing_data_handling": "impact_evaluation_analysis_missing_data_handling"
    # "impact_fidelity"?? # choices field
    # "impact_description_planned_analysis" ??
    # Process evaluation design
    # "process_methods":
    # TODO - fields don't match
    # "process_analysis_description"
    # Economic evaluation design
    # "economic_type"
    # "perspective_costs"
    # "perspective_benefits"
    # "monetisation_approaches"
    # "economic_design_details"
    # Economic evaluation analysis
    # "economic_analysis_description"
    "other_design_type": "other_evaluation_design_other_evaluation_design",
    "other_design_details": "other_evaluation_design_summary_of_methods",
    "other_analysis_description": "other_evaluation_design_description_of_analysis",
    # Impact evaluation findings - TODO - how dow these match?
    # impact_comparison
    # impact_outcome
    # impact_interpretation
    # impact_point_estimate_diff
    # impact_lower_uncertainty
    # impact_upper_uncertainty
    # # Economic evaluation findings
    "economic_summary_findings": "economic_evaluation_findings_summary_findings",
    "economic_findings": "economic_evaluation_findings_findings",
    # # Process evaluation findings
    # process_summary_findings
    # process_findings
    # # Other evaluation findings
    "other_summary_findings": "other_evaluation_findings_summary_findings",
    "other_findings": "other_evaluation_findings_findings",
}

INTERVENTION_MAPPING = {
    "name": "intervention_intervention_name",
    "brief_description": "intervention_intervention_brief_description",
    "rationale": "intervention_intervention_rationale",
    "materials_used": "intervention_materials_used",
    "procedures": "intervention_procedures_used",
    "provider_description": "intervention_who_delivered_the_intervention",
    "modes_of_delivery": "intervention_how_was_the_intervention_delivered",
    "location": "intervention_where_was_the_intervention_delivered",
    "frequency_of_delivery": "intervention_how_often_the_intervention_was_delivered",
    "tailoring": "intervention_tailoring",
    "fidelity": "intervention_how_well_it_was_delivered_(fidelity)",
    "resource_requirements": "intervention_resource_requirements",
    "geographical_information": "intervention_geographical_information",
}

DOCUMENTS_MAPPING = {
    "title": "evaluation_information_report_title",
    "url": "metadata_gov_uk_link",
    "description": "metadata_description",
    # "document_types" - TODO choices field
    # document_type_other"
}

PROCESSES_STANDARDS_MAPPING = {
    "name": "processes_and_standards_name_of_standard_or_process",
    # "conformity": "processes_and_standards_conformity", TODO - choices field
    "description": "processes_and_standards_description",
}

# TODO - check these
EXISTING_ORGANISATION_MAPPING = {v: k for k, v in dict(enums.org_tuples).items()}
OTHER_ORGANISATION_MAPPING = {
    "Department for Transport": "department-for-transport",
    "Closed organisation: Ministry of Housing, Communities & Local Government": "ministry-of-housing-communities-and-local-government",
    "Department for Levelling Up, Housing and Communities": "department-for-levelling-up-housing-and-communities",
    "Department for Business, Energy & Industrial Strategy": "department-for-business-energy-and-industrial-strategy",
    "Closed organisation: UK Commission for Employment and Skills": "uk-commission-for-employment-and-skills",
}
ALL_ORG_MAPPING = {**EXISTING_ORGANISATION_MAPPING, **OTHER_ORGANISATION_MAPPING}


# MANY OF THESE:
# - Evaluation costs and budget
# - Event dates
# - Outcome measure
# - Other measure
# - Processes and standards


def get_all_upload_data(filename):
    full_path = DATA_DIR / filename
    data = pd.read_excel(full_path, sheet_name=None, header=[0, 1])
    sheet_names = list(data.keys())
    relevant_sheet_names = [i for i in sheet_names if i.isdigit()]
    relevant_data = {n: df for n, df in data.items() if n in relevant_sheet_names}
    return relevant_data


def tidy_column_titles(df):
    df.columns = df.columns.to_flat_index()
    df.columns = ["_".join(col).strip() for col in df.columns.values]
    df.columns = [col.replace("/", " ") for col in df.columns.values]
    df.columns = [col.replace("  ", " ") for col in df.columns.values]
    df.columns = [col.replace(" ", "_") for col in df.columns.values]
    df.columns = [col.lower() for col in df.columns.values]
    assert len(df.columns) == 142
    return df


def get_all_upload_data_df(filename):
    data = get_all_upload_data(filename)
    all_dfs = list(data.values())
    transformed_dfs = [tidy_column_titles(df) for df in all_dfs]
    df = pd.concat(transformed_dfs)
    df = df.replace(INFO_NOT_IDENTIFIED, math.nan)
    df = df[~df["metadata_evaluation_id"].isnull()]
    df["metadata_evaluation_id"] = df["metadata_evaluation_id"].astype("int")
    df["metadata_report_id"] = df["metadata_report_id"].astype("int")
    evaluation_ids = df["metadata_evaluation_id"].unique()
    evaluation_ids = [id for id in evaluation_ids if not math.isnan(id)]
    return evaluation_ids, df


def get_data_for_field(evaluation_df, fieldname_in_rsm):
    """Standard field in evaluation ie one field, may need to aggregate data,
    though in most cases there will only be one value."""
    data_for_field = evaluation_df[fieldname_in_rsm]
    all_non_null_data = data_for_field.dropna(how="all")
    all_non_null_data = all_non_null_data.unique()
    string_summary = "/n".join(all_non_null_data)
    return string_summary


def get_evaluation_types(evaluation_df):
    evaluation_types = []
    other_detail = ""
    if "Y" in evaluation_df["evaluation_information_process"].unique():
        evaluation_types.append(choices.EvaluationTypeOptions.PROCESS.value)
    if "Y" in evaluation_df["evaluation_information_impact"].unique():
        evaluation_types.append(choices.EvaluationTypeOptions.IMPACT.value)
    if "Y" in evaluation_df["evaluation_information_economic"].unique():
        evaluation_types.append(choices.EvaluationTypeOptions.ECONOMIC.value)

    others = evaluation_df["evaluation_information_other_evaluation_type_(please_state)"].dropna()
    others = others.unique()
    others = set(others).difference({"N", "N/A"})
    if others:
        evaluation_types.append(choices.EvaluationTypeOptions.OTHER.value)
        if len(others) > 1:
            print(f"More than one other evaluation type: {others}")  # noqa
        # TODO - can there be more than one? Unlikely
        evaluation_types.append(choices.EvaluationTypeOptions.OTHER.value)
        other_detail = ";".join(others)
    return evaluation_types, other_detail


def get_organisations(evaluation_df):
    all_vals = evaluation_df["metadata_orgs_titles"].dropna(how="all")
    all_vals = all_vals.unique()
    try:
        converted_vals = [ALL_ORG_MAPPING[org] for org in all_vals]
    except KeyError:
        print(f"Non-matching org: {all_vals}")  # noqa
        converted_vals = []
    return converted_vals


def save_intervention_data(evaluation, evaluation_df):
    intervention_df = evaluation_df[list(INTERVENTION_MAPPING.values())]
    intervention_df = intervention_df.dropna(how="all")
    for _, row in intervention_df.iterrows():
        intervention = models.Intervention(evaluation=evaluation)
        intervention.save()
        for k, v in INTERVENTION_MAPPING.items():
            setattr(intervention, k, row[v])
            intervention.save()


def save_document_data(evaluation, evaluation_df):
    document_df = evaluation_df[list(DOCUMENTS_MAPPING.values())]
    document_df = document_df.dropna(how="all")
    for _, row in document_df.iterrows():
        document = models.Document(evaluation=evaluation)
        document.save()
        for k, v in DOCUMENTS_MAPPING.items():
            setattr(document, k, row[v])
            document.save()


def save_process_standard_data(evaluation, evaluation_df):
    df = evaluation_df[list(PROCESSES_STANDARDS_MAPPING.values())]
    df = df.dropna(how="all")
    for _, row in df.iterrows():
        process_standard = models.ProcessStandard(evaluation=evaluation)
        process_standard.save()
        for k, v in PROCESSES_STANDARDS_MAPPING.items():
            setattr(process_standard, k, row[v])
            process_standard.save()


def upload_data_for_id(all_df, rsm_id):
    evaluation_df = all_df[all_df["metadata_evaluation_id"] == rsm_id]
    evaluation, created = models.Evaluation.objects.get_or_create(rsm_id=rsm_id)
    evaluation.status = choices.EvaluationVisibility.PUBLIC.value
    # Add standard fields
    for model_field_name, rsm_field_name in EVALUATION_STANDARD_FIELDS_LOOKUP.items():
        value = get_data_for_field(evaluation_df, rsm_field_name)
        setattr(evaluation, model_field_name, value)
    evaluation.save()
    evaluation.evaluation_type, evaluation.evaluation_type_other = get_evaluation_types(evaluation_df)
    evaluation.organisations = get_organisations(evaluation_df)
    if not created:  # Do this to avoid duplicates, no other way of identifying the related objects
        evaluation.interventions.all().delete()
        evaluation.documents.all().delete()
        evaluation.process_standards.all().delete()
    save_intervention_data(evaluation, evaluation_df)
    save_document_data(evaluation, evaluation_df)
    save_process_standard_data(evaluation, evaluation_df)
    # Add number fields
    # Add choice fields
    # Add remaining one-to-many objects
    # TODO - where are the outcome/other measures
    evaluation.page_statuses = {}
    evaluation.save()


def upload_all_data(filename):
    try:
        evaluation_ids, df = get_all_upload_data_df(filename)
        for id in evaluation_ids:
            upload_data_for_id(df, id)
            print(f"Imported evaluation with id: {id}")  # noqa
        print("Done import!")  # noqa
    except FileNotFoundError:
        print(f"Import unsuccessful - incorrect filename: {filename} \nEnsure data is in the `data` folder")  # noqa


# COLUMNS from Excel - as yet, unmatched fields
# Index(['metadata_evaluation_id', 'metadata_report_id',
#        'metadata_evaluation_name',

#        'metadata_display_type',
#    'metadata_format',
#        'metadata_link', 'metadata_public_timestamp', 'metadata_document_type',
#        'metadata_orgs_titles', 'metadata_final_categorisation',
#        'evaluation_information_evaluation_id',
#        'evaluation_information_report_id',

#        'evaluation_information_report_type',
#        'evaluation_information_government_department__client',
#        'evaluation_information_author(s)',

#        'evaluation_information_intervention_start_date_(month)',
#        'evaluation_information_intervention_start_date_(year)',
#        'evaluation_information_intervention_end_date_(month)',
#        'evaluation_information_intervention_end_date_(year)',
#        'evaluation_information_processes_and_standards',
#        'evaluation_information_evaluation_cost_(£)',
#        'evaluation_information_publication_date_(month)',
#        'evaluation_information_publication_date_(year)',
#        'evaluation_event_dates_event_category',
#        'evaluation_event_dates_event_start_date_(month)',
#        'evaluation_event_dates_event_start_date_(year)',
#        'evaluation_event_dates_event_end_date_(month)',
#        'evaluation_event_dates_event_end_date_(year)',

#        'intervention_intervention_costs_(£)',

#        'process_evaluation_design_design', 'process_evaluation_design_method',
#        'process_evaluation_design_method_sample_size',
#        'process_evaluation_design_method_sample_size_process',
#        'process_evaluation_design_description',
#        'process_evaluation_design_rationale_for_chosen_methods',

#        'impact_evaluation_design_method_sample_size',
#        'impact_evaluation_design_method_sample_size_process',

#        'economic_evaluation_design_methods'],

# Index(['economic_evaluation_design_method_sample_size',
#        'economic_evaluation_design_method_sample_size_process',
#        'economic_evaluation_design_costs_included',
#        'economic_evaluation_design_benefits_included',
#        'economic_evaluation_design_monetisation_approach(es)',
#        'economic_evaluation_design_description_of_economic_evaluation_design',

#       'impact_evaluation_findings_summary_findings',
#        'impact_evaluation_findings_findings',

#        'ethical_considerations_ethics_approval_applied_for',
