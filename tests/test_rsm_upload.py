from etf.evaluation import models
from etf.evaluation.management.commands.upload_rsm_data import transform_and_create_from_rows

headers = [
    "Evaluation ID",
    "Report ID",
    "gov_uk_link",
    "Evaluation title",
    "Short title for evaluation",
    "Process",
    "Impact",
    "Economic",
    "Other evaluation type (please state)",
    "Report title",
    "Report type",
    "Government departments",
    "Author(s)",
    "Evaluation summary",
    "Intervention start date (Month)",
    "Intervention start date (Year)",
    "Intervention end date (Month)",
    "Intervention end date (Year)",
    "Processes and standards",
    "Evaluation cost (£)",
    "Publication date (Month)",
    "Publication date (Year)",
    "Links to associated docments",
    "Event category",
    "Event start date (Month)",
    "Event start date (Year)",
    "Event end date (Month)",
    "Event end date (Year)",
    "Issue to be addressed",
    "Who is experiencing the issue",
    "Current practice",
    "Why the issue is important / why are improvements needed",
    "Who does it matter to",
    "What difference the intervention intends to make",
    "Studied population including location(s)",
    "Eligibility criteria",
    "Total number of people (or other unit) included in the evaluation",
    "Type of unit",
    "Intervention name",
    "Intervention brief description",
    "Intervention rationale",
    "Materials used",
    "Procedures used",
    "Who delivered the intervention",
    "How was the intervention delivered",
    "Where was the intervention delivered",
    "How often the intervention was delivered",
    "Tailoring",
    "How well it was delivered (fidelity)",
    "Resource requirements",
    "Geographical information",
    "Intervention costs (£)",
    "Referral / recruitment route",
    "Referral / recruitment schedule",
    "Process - Design",
    "Process - Method",
    "Process - Method sample size",
    "Process - Method sample size process",
    "Process - Description",
    "Process - Rationale for chosen methods",
    "Impact - Design",
    "Impact - Justification for design",
    "Impact - Features to reflect real-world implementation",
    "Impact - Description",
    "Impact - Equity",
    "Impact - Method sample size",
    "Impact - Method sample size process",
    "Impact - Assumptions",
    "Impact - Limitations of approach",
    "Economic - Methods",
    "Economic - Method sample size",
    "Economic - Method sample size process",
    "Economic - Costs included",
    "Economic - Benefits included",
    "Economic - Monetisation approach",
    "Economic - Evaluation design",
    "Other - Evaluation design",
    "Other - Summary of methods",
    "Process - Description of analysis",
    "Impact - Analysis framework",
    "Impact - Analysis basis",
    "Impact - Analysis set",
    "Impact - Primary effect size measure type",
    "Impact - Primary effect size measure",
    "Impact - Primary effect size measure interval",
    "Impact - Primary effect size measure description",
    "Impact - Interpretation type",
    "Impact - Sensitivity analysis",
    "Impact - Subgroup analysis",
    "Impact - Missing data handling",
    "Impact - Fidelity of report",
    "Impact - Description of analysis",
    "Economic - Description of analysis",
    "Other - Description of analysis",
    "Outcome title",
    "Primary or secondary outcome",
    "Direct or surrogate",
    "Measure type",
    "Description of measure",
    "Collection procedures",
    "Time point of intesest (Month)",
    "Time point of intesest (Year)",
    "Minimum practically important difference",
    "Relevance of outcome",
    "Other outcomes - Outcome name",
    "Other outcomes - Outcome measure type",
    "Other outcomes - Description of measure",
    "Other outcomes - Collection procedures and timing",
    "Process - Summary of findings",
    "Process - Findings",
    "Impact - Summary of findings",
    "Impact - Findings",
    "Economic - Summary of findings",
    "Economic - Findings",
    "Other - Summary of findings",
    "Other - Findings",
    "Ethics approval applied for",
    "Ethics committee approval",
    "Ethics committee details",
    "Ethical state of study given existing evidence base",
    "Risks to participants",
    "Risks to study team",
    "Participant involvement",
    "Participant consent (if no, why not)",
    "Participant information",
    "Participant payment (if yes, please ellaborate)",
    "Confidentiality and personal data",
    "Breaking confidentiality",
    "Other ethical information",
    "Name of standard or process",
    "Conformity",
    "Process and standards - Description",
]

data_row = [
    [
        "1",  # eval id
        "1",  # report id
        "https://www.google.com/",  # govuk link
        "Evaluation title",  # eval title
        "Short evaluation title",  # short title
        "N",  # process eval
        "Y",  # impact eval
        "N",  # economic eval
        "N",  # other eval
        "Report title",  # report title
        "Report type",  # report type
        "Department for Transport",  # organisation
        "Author name",  # author name
        "A summary of the evaluation",  # eval summary
        "Jul",  # intervention start month
        "2011",  # intervention start year
        "Mar",  # intervention end month
        "2015",  # intervention end year
        "A simple process and standard",  # process and standard
        "1000",  # evaluation cost
        "Dec",  # publication date month
        "2016",  # publication date year
        "",  # link to associated document
        "Analysis",  # event category
        "Information not identified within the report",  # event start month
        "2012",  # event start year
        "Information not identified within the report",  # event end month
        "2014",  # event end year
        "Issue to be addressed",  # issue to be addressed
        "Those experiencing the issue",  # who is experiencing the issue
        "Information not announced in the report",  # current practice
        "Why is it important",  # why is it important / needed
        "Department for Transport",  # who does it matter to
        "Example text",  # what difference it makes
        "People",  # studied population
        "Visitors to the area",  # eligibility criteria
        "186",  # total number of people in the evaluation
        "people",  #  unit type
        "Local Sustainable Transport Fund",  # intervention name
        "Intervention brief description",  # intervention brief description
        "Rationale for the intervention",  # intervention rationale
        "Materials used",  # intervention materials used
        "Procedures used for the intervention",  # intervention procedures used
        "The person who delivered it",  # who delivered the intervention
        "How was it delivered",  # how was the intervention delivered
        "Where the intervention was delivered",  # where was the intervention delivered
        "How often the intervention was delivered",  # how often was the intervention delivered
        "Tailoring",  # tailoring
        "How well was it delivered",  # how well it was delivered (fidelity)
        "Resource requirements",  # resource requirements
        "England",  # geographical information
        "£69m funding programme",  # intervention cost
        "Recruitment route",  # referral / recruitment route
        "Recruitment schedule",  # referral / recruitment schedule
        "Process design",  # process design
        "Process method",  # process method
        "20",  # process method sample size
        "Process sample size process",  # process method sample size process
        "Process description",  # process description
        "Process rationale",  # process rationale for chosen method
        "Output or performance monitoring",  # impact design
        "Justification for design",  # impact justification for design
        "Features that reflect the real world",  # impact features to reflect real world implementation
        "Impact description",  # impact description
        "Impact equity",  # impact equity
        "440",  # impact method sample size
        "Impact sample size process",  # impact method sample size process
        "Impact assumptions",  # impact assumptions
        "Due to the limitations of both time and budget...",  # impact limitations of approach
        "Economic method",  # economic methods
        "340",  # economic method sample size
        "Sample size process",  # economic method sample size process
        "A lot of costs that are included",  # economic costs included
        "Some benefits included",  # economic benefits included
        "Economic monetisation approach",  # economic monetisation approach
        "Economic evaluation design",  # economic evaluation design
        "Other evaluation design",  # other evaluation design
        "Other summary of methods",  # other summary of methods
        "Process description of analysis",  # process description of analysis
        "Superiority",  # impact analysis framework
        "Impact analysis basis",  # impact analysis basis
        "Interviewed 300 businesses",  # impact analysis set
        "Relative measure",  # impact primary effect size measure type
        "Numerical outcome",  # impact primary effect size measure
        "Confidence interval",  # impact primary effect size measure interval
        "Primary effect measure description",  # impact primary effect size measure description
        "Interpretation of intervals",  # impact interpretation type
        "Impact sensitivity analysis",  # impact sensitivity analysis
        "Subgroup analysis",  # impact subgroup analysis
        "Data handling",  # impact missing data handling
        "Yes",  # impact fidelity of report
        "Description of analysis",  # impact description of analysis
        "Economic description of analysis",  # economic description of analysis
        "Other description of analysis",  # other description of analysis
        "Reduced congestion",  # outcome title
        "Primary",  # primary of secondary outcome
        "Direct",  # direct or surrogate
        "Continuous",  # measure type
        "average daily traffic counts",  # description of measure
        "Case study",  # collection procedures
        "feb",  # timepoint of interest month
        "2014",  # timepoint of interest year
        "Minimum difference",  # minimum practically important difference
        "Relevance of outcome",  # relevance of outcome
        "Another outcome",  # other outcome name
        "DISCRETE",  # other outcome measure type
        "A small description",  # other outcome description of measure
        "Timing",  # other outcome collection procedures and timing
        "Process summary of findings",  # process summary of findings
        "Process findings",  # process findings
        "Impact summary findings",  # impact summary findings
        "Impact findings",  # impact findings
        "Economic summary of findings",  # economic summary of findings
        "Economic findings",  # economic findings
        "Other summary of findings",  # other summary of findings
        "Other findings",  # other findings
        "Y",  # ethical approval applied for
        "N",  # ethics committee approval
        "A small ethical question",  # ethics committee details
        "Ethical evidence base",  # ethical state of a study given existing evidence base
        "Risks to participants",  # risks to participants
        "Risks to study team",  # risks to study team
        "Participant involvement",  # participant involvement
        "N",  # participant consent
        "Participant information",  # participant information
        "Participant payment",  # participant payment
        "Confidentiality and personal info",  # confidentiality and personal data
        "Breaking confidentiality",  # breaking confidentiality
        "Other ethical info",  # other ethical information
        "Name of standard or process",  # name of standard or process
        "Conformity",  # conformity
        "Process and standards description",  # process and standards description
    ],
]


def test_upload_evaluation():
    evaluations = models.Evaluation.objects.all()
    evaluations.delete()
    transform_and_create_from_rows(data_row, headers)
    # print(data_row[0][headers.index("Impact - Analysis set")])
    evaluation = models.Evaluation.objects.first()
    assert evaluation.title == "Evaluation title", evaluation.title
    assert evaluation.short_title == "Short evaluation title", evaluation.short_title
    assert evaluation.evaluation_type == ["IMPACT"], evaluation.evaluation_type
    assert evaluation.organisations == ["department-for-transport"], evaluation.organisations
    assert evaluation.brief_description == "A summary of the evaluation.", evaluation.brief_description
    assert evaluation.issue_description_option == "YES", evaluation.issue_description_option
    assert evaluation.ethics_option == "YES", evaluation.ethics_option
    assert evaluation.grants_option == "NO", evaluation.grants_option
    assert evaluation.issue_description == "Issue to be addressed.", evaluation.issue_description
    assert evaluation.those_experiencing_issue == "Those experiencing the issue.", evaluation.those_experiencing_issue
    assert evaluation.why_improvements_matter == "Why is it important.", evaluation.why_improvements_matter
    assert evaluation.who_improvements_matter_to == "Department for Transport.", evaluation.who_improvements_matter_to
    assert evaluation.current_practice is None, evaluation.current_practice
    assert evaluation.issue_relevance == "Example text.", evaluation.issue_relevance
    assert evaluation.evaluation_type_other is None, evaluation.evaluation_type_other
    assert evaluation.studied_population == "People.", evaluation.studied_population
    assert evaluation.eligibility_criteria == "Visitors to the area.", evaluation.eligibility_criteria
    # assert evaluation.sample_size == 186, evaluation.sample_size  # Sample size not being set
    assert evaluation.sample_size_units == "people", evaluation.sample_size_units
    assert evaluation.sample_size_details is None, evaluation.sample_size_details
    assert evaluation.process_for_recruitment == "Recruitment route.", evaluation.process_for_recruitment

    assert evaluation.recruitment_schedule == "Recruitment schedule.", evaluation.recruitment_schedule
    assert evaluation.ethics_committee_approval == "NO", evaluation.ethics_committee_approval
    assert evaluation.ethics_committee_details == "A small ethical question.", evaluation.ethics_committee_details
    assert (
        evaluation.ethical_state_given_existing_evidence_base == "Ethical evidence base."
    ), evaluation.ethical_state_given_existing_evidence_base
    assert evaluation.risks_to_participants == "Risks to participants.", evaluation.risks_to_participants
    assert evaluation.risks_to_study_team == "Risks to study team.", evaluation.risks_to_study_team
    assert evaluation.participant_involvement == "Participant involvement.", evaluation.participant_involvement
    assert evaluation.participant_information == "Participant information.", evaluation.participant_information
    assert evaluation.participant_consent == "N", evaluation.participant_consent
    assert evaluation.participant_payment == "Participant payment.", evaluation.participant_payment
    # assert evaluation.confidentiality_and_personal_data == "Confidentiality and personal info.", evaluation.confidentiality_and_personal_data  # Not setting
    assert evaluation.breaking_confidentiality == "Breaking confidentiality.", evaluation.breaking_confidentiality
    assert evaluation.other_ethical_information == "Other ethical info.", evaluation.other_ethical_information

    assert evaluation.impact_design_name == ["OUTPUT_OR_PERFORMANCE_MONITORING"], evaluation.impact_design_name
    assert evaluation.impact_design_name_other is None, evaluation.impact_design_name_other
    assert evaluation.impact_design_justification == "Justification for design.", evaluation.impact_design_justification
    assert evaluation.impact_design_description == "Impact description.", evaluation.impact_design_description
    assert (
        evaluation.impact_design_features == "Features that reflect the real world."
    ), evaluation.impact_design_features
    assert evaluation.impact_design_equity == "Impact equity.", evaluation.impact_design_equity
    assert evaluation.impact_design_assumptions == "Impact assumptions.", evaluation.impact_design_assumptions
    assert (
        evaluation.impact_design_approach_limitations == "Due to the limitations of both time and budget."
    ), evaluation.impact_design_approach_limitations

    assert evaluation.impact_framework == "SUPERIORITY", evaluation.impact_framework
    assert evaluation.impact_framework_other is None, evaluation.impact_framework_other
    # assert evaluation.impact_basis == "Impact analysis basis.", evaluation.impact_basis  # not setting
    assert evaluation.impact_basis_other is None, evaluation.impact_basis_other
    # assert evaluation.impact_analysis_set == "interviewed 300 businesses.", evaluation.impact_analysis_set # not being set properly
    assert evaluation.impact_effect_measure_type == "RELATIVE", evaluation.impact_effect_measure_type
    assert evaluation.impact_effect_measure_type_other is None, evaluation.impact_effect_measure_type_other
    assert (
        evaluation.impact_primary_effect_size_measure == "Numerical outcome."
    ), evaluation.impact_primary_effect_size_measure
    assert evaluation.impact_effect_measure_interval == "CONFIDENCE", evaluation.impact_effect_measure_interval
    assert evaluation.impact_effect_measure_interval_other is None, evaluation.impact_effect_measure_interval_other
    assert evaluation.impact_primary_effect_size_desc == "Primary effect measure description.", evaluation.impact_primary_effect_size_desc
    assert evaluation.impact_interpretation_type == "INTERVALS", evaluation.impact_interpretation_type
    assert evaluation.impact_interpretation_type_other is None, evaluation.impact_interpretation_type_other
    # assert evaluation.impact_sensitivity_analysis == "Impact sensitivity analysis.", evaluation.impact_sensitivity_analysis  # Not setting correctly
    # assert evaluation.impact_subgroup_analysis == "Subgroup analysis.", evaluation.impact_subgroup_analysis  # Not setting
    assert evaluation.impact_missing_data_handling == "Data handling.", evaluation.impact_missing_data_handling
    assert evaluation.impact_fidelity == "YES", evaluation.impact_fidelity
    # assert evaluation.impact_description_planned_analysis == "Description of analysis.", evaluation.impact_description_planned_analysis  # Not setting correctly

    assert evaluation.economic_type is None, evaluation.economic_type
    assert evaluation.perspective_costs == "A lot of costs that are included.", evaluation.perspective_costs
    assert evaluation.perspective_benefits == "Some benefits included.", evaluation.perspective_benefits  # not being set
    assert evaluation.monetisation_approaches == "Economic monetisation approach.", evaluation.monetisation_approaches
    assert evaluation.economic_design_details == "Economic evaluation design.", evaluation.economic_design_details

    # assert evaluation.economic_analysis_description == "Economic description of analysis.", evaluation.economic_analysis_description  # not setting

    assert evaluation.other_design_type == "Other evaluation design.", evaluation.other_design_type

    # assert evaluation.other_analysis_description == "Other description of analysis.", evaluation.other_analysis_description

    assert evaluation.impact_comparison is None, evaluation.impact_comparison
    assert evaluation.impact_outcome is None, evaluation.impact_outcome
    assert evaluation.impact_interpretation is None, evaluation.impact_interpretation
    assert evaluation.impact_interpretation_other is None, evaluation.impact_interpretation_other
    assert evaluation.impact_point_estimate_diff is None, evaluation.impact_point_estimate_diff
    assert evaluation.impact_lower_uncertainty is None, evaluation.impact_lower_uncertainty
    assert evaluation.impact_upper_uncertainty is None, evaluation.impact_upper_uncertainty

    assert evaluation.economic_summary_findings == "Economic summary of findings.", evaluation.economic_summary_findings
    assert evaluation.economic_findings == "Economic findings.", evaluation.economic_findings

    assert evaluation.other_summary_findings == "Other summary of findings.", evaluation.other_summary_findings
    assert evaluation.other_findings == "Other findings.", evaluation.other_findings

    assert False
