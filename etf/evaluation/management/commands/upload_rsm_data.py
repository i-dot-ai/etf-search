import csv
import pathlib
from collections import defaultdict

import httpx
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.core.management.base import BaseCommand
from django.db import DataError

from etf.evaluation import choices, models

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
    AlternateChoice(label="Y", name=choices.YesNo.YES.name),
    AlternateChoice(label="Y (AA)", name=choices.YesNo.YES.name),
    AlternateChoice(label="Yes", name=choices.YesNo.YES.name),
    AlternateChoice(label="N", name=choices.YesNo.NO.name),
    AlternateChoice(label="No", name=choices.YesNo.NO.name),
)

impact_design_name_choices = (
    AlternateChoice(label="surveys and polling", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="individual interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name),
    AlternateChoice(
        label="output or performance monitoring", name=choices.ImpactEvalDesign.OUTPUT_OR_PERFORMANCE_MONITORING.name
    ),
    AlternateChoice(label="Randomised Controlled Trial (RCT)", name=choices.ImpactEvalDesign.RCT.name),
    AlternateChoice(label="Interviews and group sessions", name=choices.ImpactEvalDesign.FOCUS_GROUPS.name),
    AlternateChoice(label="Surveys (ECTs)", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Cluster randomised RCT", name=choices.ImpactEvalDesign.CLUSTER_RCT.name),
    AlternateChoice(
        label="Surveys, focus groups and interviews conducted", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name
    ),
    AlternateChoice(label="Propensity Score Matching", name=choices.ImpactEvalDesign.PROPENSITY_SCORE_MATCHING.name),
    AlternateChoice(
        label="Focus groups or group interviews alongwith individual interviews & case studies",
        name=choices.ImpactEvalDesign.FOCUS_GROUPS.name,
    ),
    AlternateChoice(label="Difference in Difference", name=choices.ImpactEvalDesign.DIFF_IN_DIFF.name),
    AlternateChoice(
        label="Output or performance review", name=choices.ImpactEvalDesign.OUTPUT_OR_PERFORMANCE_MONITORING.name
    ),
    AlternateChoice(label="Survey and polling", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Individual interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name),
    AlternateChoice(label="Case studies", name=choices.ImpactEvalDesign.CASE_STUDIES.name),
    AlternateChoice(label="Survey respondents (landlords)", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Simulation model developed", name=choices.ImpactEvalDesign.SIMULATION_MODELLING.name),
    AlternateChoice(label="Focus groups or group interviews", name=choices.ImpactEvalDesign.FOCUS_GROUPS.name),
    AlternateChoice(label="Outcome letter review", name=choices.ImpactEvalDesign.OUTCOME_HARVESTING.name),
    AlternateChoice(label="Semi structured qualitative interviews", name=choices.ImpactEvalDesign.QCA.name),
    AlternateChoice(
        label="Other (Qualitative research)", name=choices.ImpactEvalDesign.QUALITATIVE_OBSERVATIONAL_STUDIES.name
    ),
    AlternateChoice(
        label="Mix of methods including surveys and group interviews",
        name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name,
    ),
    AlternateChoice(
        label="Telephone interviews (housing advisers)", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name
    ),
    AlternateChoice(label="Individual interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name),
    AlternateChoice(label="Focus groups, interviews, and surveys", name=choices.ImpactEvalDesign.FOCUS_GROUPS.name),
    AlternateChoice(
        label="Review of data from Adult Tobacco Policy Survey", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name
    ),
    AlternateChoice(label="Consultative/deliberative methods", name=choices.ImpactEvalDesign.CONSULTATIVE_METHODS.name),
    AlternateChoice(label="Surveys (senior leaders)", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Randomised Controlled Trial", name=choices.ImpactEvalDesign.RCT.name),
    AlternateChoice(label="Synthetic Control Methods", name=choices.ImpactEvalDesign.SYNTHETIC_CONTROL_METHODS.name),
    AlternateChoice(label="interviews", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name),
    AlternateChoice(
        label="qualitative depth interviews and focus groups",
        name=choices.ImpactEvalDesign.QUALITATIVE_OBSERVATIONAL_STUDIES.name,
    ),
    AlternateChoice(label="Case Studies", name=choices.ImpactEvalDesign.CASE_STUDIES.name),
    AlternateChoice(label="Case studies and interviews", name=choices.ImpactEvalDesign.CASE_STUDIES.name),
    AlternateChoice(label="Simulation modelling", name=choices.ImpactEvalDesign.SIMULATION_MODELLING.name),
    AlternateChoice(label="Focus group", name=choices.ImpactEvalDesign.FOCUS_GROUPS.name),
    AlternateChoice(label="Interviews (landlords)", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name),
    AlternateChoice(label="Process Tracing", name=choices.ImpactEvalDesign.PROCESS_TRACING.name),
    AlternateChoice(label="Interview", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name),
    AlternateChoice(
        label="regression adjusted Difference-in-Difference (DiD)", name=choices.ImpactEvalDesign.DIFF_IN_DIFF.name
    ),
    AlternateChoice(label="Survyes and case study", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Participant Survey", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="focus groups", name=choices.ImpactEvalDesign.FOCUS_GROUPS.name),
    AlternateChoice(label="INTERVIEW", name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name),
    AlternateChoice(label="Surveys and polling", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Surveys and interviews", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Focus groups (housing advisers)", name=choices.ImpactEvalDesign.FOCUS_GROUPS.name),
    AlternateChoice(label="Forcus group", name=choices.ImpactEvalDesign.FOCUS_GROUPS.name),
    AlternateChoice(label="Contribution Tracing", name=choices.ImpactEvalDesign.CONTRIBUTION_TRACING.name),
    AlternateChoice(label="Surveys", name=choices.ImpactEvalDesign.SURVEYS_AND_POLLING.name),
    AlternateChoice(label="Outcome harvesting", name=choices.ImpactEvalDesign.OUTCOME_HARVESTING.name),
    AlternateChoice(
        label="Performance or output monitoring", name=choices.ImpactEvalDesign.OUTPUT_OR_PERFORMANCE_MONITORING.name
    ),
    AlternateChoice(
        label="Individual interviews along with surveys and review of monitoring data to carry out quantitative modelling approach",
        name=choices.ImpactEvalDesign.INDIVIDUAL_INTERVIEWS.name,
    ),
    AlternateChoice(
        label="Simulation modelling: Asset Liability Modelling (ALM)",
        name=choices.ImpactEvalDesign.SIMULATION_MODELLING.name,
    ),
    AlternateChoice(label="Other (RCT - Quasi-Experimentl approaches)", name=choices.ImpactEvalDesign.RCT.name),
)


organisation_choices = (
    AlternateChoice(
        label="Social Mobility & Child Poverty Commission", name="social-mobility-and-child-poverty-commission"
    ),
    AlternateChoice(label="Other (Department of Health)", name="department-of-health-and-social-care"),
    AlternateChoice(
        label="Department for Science, Innovation & Technology", name="department-for-science-innovation-and-technology"
    ),
    AlternateChoice(label="Department of Health and Social Care", name="department-of-health-and-social-care"),
    AlternateChoice(label="HM Treasury (HMT)", name="hm-treasury"),
    AlternateChoice(
        label="Department for Digital, Culture, Media & Sport; Office for Artificial Intelligence",
        name="department-for-digital-culture-media-sport",
    ),
    AlternateChoice(
        label="Department for Science, Innovation and Technology",
        name="department-for-science-innovation-and-technology",
    ),
    AlternateChoice(label="Innovate UK", name="innovate-uk"),
    AlternateChoice(
        label="Department of Agriculture, Environment and Rural Affairs",
        name="department-of-agriculture-and-rural-development",
    ),
    AlternateChoice(label="Environment Agency", name="environment-agency"),
    AlternateChoice(label="Ofqual", name="ofqual"),
    AlternateChoice(
        label="Department of Energy and Climate Change (DECC) and BIS", name="department-of-energy-climate-change"
    ),
    AlternateChoice(
        label="Youth Justice Board for England and Wales", name="youth-justice-board-for-england-and-wales"
    ),
    AlternateChoice(
        label="Department of Health and Social Care, Department for Education and NHS England and Improvement",
        name="department-of-health-and-social-care",
    ),
    AlternateChoice(label="The British Business Bank", name="british-business-bank"),
    AlternateChoice(label="Nuclear Waste Services", name="nuclear-waste-services"),
    AlternateChoice(
        label="Department for Energy Security & Net Zero", name="department-for-energy-security-and-net-zero"
    ),
    AlternateChoice(label="Highways England", name="highways-england"),
    AlternateChoice(label="HM Prison and Probation Service", name="hm-prison-and-probation-service"),
    AlternateChoice(
        label="Department for Energy Security and Net Zero", name="department-for-energy-security-and-net-zero"
    ),
    AlternateChoice(
        label="Office for Health Improvement and Disparities", name="office-for-health-improvement-and-disparities"
    ),
    AlternateChoice(label="Department of Health", name="department-of-health-and-social-care"),
    AlternateChoice(label="Department for Education", name="department-for-education"),
    AlternateChoice(label="NIHR", name="northern-ireland-human-rights-commission"),
    AlternateChoice(
        label="Department for Digital, Culture, Media & Sport", name="department-for-digital-culture-media-sport"
    ),
    AlternateChoice(
        label="Department for Environment, Food & Rural Affairs", name="department-for-environment-food-rural-affairs"
    ),
    AlternateChoice(label="Department for Transport", name="department-for-transport"),
    AlternateChoice(label="Government Social Research", name="civil-service-government-social-research-profession"),
    AlternateChoice(label="Uk Trade & Investment", name="uk-trade-investment"),
    AlternateChoice(
        label="Department for Levelling Up, Housing and Communities",
        name="department-for-levelling-up-housing-and-communities",
    ),
    AlternateChoice(label="Public Health England", name="public-health-england"),
    AlternateChoice(label="British Business Bank", name="british-business-bank"),
    AlternateChoice(label="Home Office", name="home-office"),
    AlternateChoice(label="UK Space Agency", name="uk-space-agency"),
    AlternateChoice(
        label="Closed organisation: Ministry of Housing, Communities & Local Government",
        name="ministry-of-housing-communities-and-local-government",
    ),
    AlternateChoice(label="Building Digital UK", name="building-digital-uk"),
    AlternateChoice(label="UK Trade & Investment", name="uk-trade-investment"),
    AlternateChoice(
        label="Department for Digital, Culture, Media and Sport", name="department-for-digital-culture-media-sport"
    ),
    AlternateChoice(label="Office of Manpower Economics | Home Office", name="office-of-manpower-economics"),
    AlternateChoice(label="Ministry of Justice | HM Prison and Probation Service", name="ministry-of-justice"),
    AlternateChoice(label="Closed organisation: Highways England", name="highways-england"),
    AlternateChoice(label="UK Research and Innovation", name="uk-research-and-innovation"),
    AlternateChoice(label="Animal and Plant Health Agency", name="animal-and-plant-health-agency"),
    AlternateChoice(label="Department of work and pensions", name="department-for-work-pensions"),
    AlternateChoice(label="Department for Business & Trade", name="department-for-business-and-trade"),
    AlternateChoice(label="Department for Culture, Media & Sport", name="department-for-culture-media-and-sport"),
    AlternateChoice(label="HM Revenue & Customs | HM Treasury", name="hm-revenue-customs"),
    AlternateChoice(
        label="Closed organisation: Department for Business, Innovation & Skills",
        name="department-for-business-innovation-skills",
    ),
    AlternateChoice(
        label="Closed organisation: Department of Energy & Climate Change", name="department-of-energy-climate-change"
    ),
    AlternateChoice(
        label="Department for Business, Energy & Industrial Strategy",
        name="department-for-business-energy-and-industrial-strategy",
    ),
    AlternateChoice(label="Office for Zero Emission Vehicles", name="office-for-zero-emission-vehicles"),
    AlternateChoice(label="HM Prison & Probation Service", name="hm-prison-and-probation-service"),
    AlternateChoice(label="Government Equalities Office", name="government-equalities-office"),
    AlternateChoice(label="Foreign, Commonwealth & Development Office", name="foreign-commonwealth-development-office"),
    AlternateChoice(label="DCMS", name="department-for-digital-culture-media-sport"),
    AlternateChoice(
        label="Department for Levelling Up, Housing & Communities",
        name="department-for-levelling-up-housing-and-communities",
    ),
    AlternateChoice(
        label="UK Commission for Employment and Skills (UKCES)", name="uk-commission-for-employment-and-skills"
    ),
    AlternateChoice(label="Department for Transport (DfT)", name="department-for-transport"),
    AlternateChoice(label="Driving Standards Agency (DSA)", name="driving-standards-agency"),
    AlternateChoice(label="Competition and Markets Authority", name="competition-and-markets-authority"),
    AlternateChoice(label="culture, media, and sport", name="department-for-culture-media-and-sport"),
    AlternateChoice(
        label="Senior Salaries Review Body",
        name="review-body-on-senior-salaries",
    ),
    AlternateChoice(label="Department of Energy and Climate Change", name="department-of-energy-climate-change"),
    AlternateChoice(label="Regulator of Social Housing", name="regulator-of-social-housing"),
    AlternateChoice(label="Closed organisation: Highways Agency", name="highways-agency"),
    AlternateChoice(label="Ofsted", name="ofsted"),
    AlternateChoice(label="Highways Agency", name="highways-agency"),
    AlternateChoice(label="Driver & Vehicle Standards Agency", name="driver-and-vehicle-standards-agency"),
    AlternateChoice(label="Closed organisation: Public Health England", name="public-health-england"),
    AlternateChoice(label="Department for Work and Pensions", name="department-for-work-pensions"),
    AlternateChoice(label="UK Health Security Agency", name="uk-health-security-agency"),
    AlternateChoice(
        label="Department for Levelling Up, Housing and Communities | Cabinet Office",
        name="department-for-levelling-up-housing-and-communities",
    ),
    AlternateChoice(label="Cabinet Office", name="cabinet-office"),
    AlternateChoice(label="Standards and Testing Agency", name="standards-and-testing-agency"),
    AlternateChoice(label="HM Revenue & Customs", name="hm-revenue-customs"),
    AlternateChoice(label="Office for Budget Responsibility", name="office-for-budget-responsibility"),
    AlternateChoice(label="UK Commission for Employment and Skills", name="uk-commission-for-employment-and-skills"),
    AlternateChoice(label="The Charity Commission", name="charity-commission"),
    AlternateChoice(label="Public Health Agency, Northern Ireland", name="public-health-agency-northern-ireland"),
    AlternateChoice(label="Department for Work and Pensions.", name="department-for-work-pensions"),
    AlternateChoice(
        label="Department for Business Innovation & Skills", name="department-for-business-innovation-skills"
    ),
    AlternateChoice(
        label="Scientific Advisory Group for Emergencies", name="scientific-advisory-group-for-emergencies"
    ),
    AlternateChoice(label="Evaluation Task Force", name="evaluation-task-force"),
    AlternateChoice(
        label="Government Social Research Profession", name="civil-service-government-social-research-profession"
    ),
    AlternateChoice(label="Ministry of Justice", name="ministry-of-justice"),
    AlternateChoice(
        label="Ministry of Housing, Communities and Local Government",
        name="ministry-of-housing-communities-and-local-government",
    ),
    AlternateChoice(label="Qualifications and Curriculum Authority", name="qualifications-and-curriculum-authority"),
    AlternateChoice(
        label="Department for Communities and Local Government",
        name="ministry-of-housing-communities-and-local-government",
    ),
    AlternateChoice(
        label="Department for Environment, Food & Rural Affairs | Home Office",
        name="department-for-environment-food-rural-affairs",
    ),
    AlternateChoice(
        label="Ministry for Housing, Communities and Local Government",
        name="ministry-of-housing-communities-and-local-government",
    ),
    AlternateChoice(
        label="Ministry of Justice and HM Prison and Probation Service", name="hm-prison-and-probation-service"
    ),
    AlternateChoice(
        label="Department for Digital, Culture Media & Sport; Arts Council England",
        name="department-for-digital-culture-media-sport",
    ),
)

supports_other = defaultdict(
    lambda: False,
    {
        yes_no_choices: False,
        organisation_choices: False,
        impact_design_name_choices: True,
        choices.EvaluationTypeOptions: True,
        choices.OutcomeType: False,
        choices.OutcomeMeasure: False,
        choices.YesNo: False,
        choices.YesNoPartial: False,
        choices.FullNoPartial: False,
        choices.MeasureType: True,
        choices.Topic: False,
        choices.EvaluationVisibility: False,
        choices.DocumentType: True,
        choices.EventDateOption: True,
        choices.EventDateType: False,
        choices.EconomicEvaluationType: False,
        choices.ImpactEvalInterpretation: True,
        choices.ImpactEvalDesign: True,
        choices.ImpactFramework: True,
        choices.ImpactAnalysisBasis: True,
        choices.ImpactMeasureInterval: True,
        choices.ImpactMeasureType: True,
        choices.ProcessEvaluationAspects: True,
        choices.ProcessEvaluationMethods: True,
    },
)


evaluation_headers = {
    "Evaluation title": {
        "field_name": "title",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Short title for evaluation": {
        "field_name": "short_title",
        "resolution_method": "single",
        "data_type": "str",
    },
    "Evaluation summary": {
        "field_name": "brief_description",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Issue to be addressed": {
        "field_name": "issue_description",
        "resolution_method": "combine",
        "data_type": "str",
    },
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
    "Eligibility criteria": {
        "field_name": "eligibility_criteria",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Total number of people (or other unit) included in the evaluation": {
        "field_name": "sample_size",
        "resolution_method": "combine",
        "data_type": "int",
    },
    "Type of unit": {
        "field_name": "sample_size_units",
        "resolution_method": "single",
        "data_type": "str",
    },
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
    "Impact - Equity": {
        "field_name": "impact_design_equity",
        "resolution_method": "combine",
        "data_type": "str",
    },
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
        "resolution_method": "combine",
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
    "Impact - Analysis set": {
        "field_name": "impact_analysis_set",
        "resolution_method": "combine",
        "data_type": "str",
    },
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
    "Participant payment (if yes, please ellaborate)": {
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
    "Government departments": {
        "field_name": "organisations",
        "resolution_method": "multiple_choice",
        "data_type": organisation_choices,
    },
}

# Organisation
# organisations_headers = {
#     "Government departments": {
#         "field_name": "organisations",
#         "resolution_method": "multiple_choice",
#         "data_type": organisation_choices,
#     }
# }

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
links_headers = [
    {
        "gov_uk_link": {
            "field_name": "name_of_service",
            "resolution_method": "single",
            "data_type": "str",
        },
    },
    {
        "gov_uk_link": {
            "field_name": "link_or_identifier",
            "resolution_method": "single",
            "data_type": "str",
        },
    },
]

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
        "data_type": "int",
    },
}

# Processes and standards
processes_and_standards_headers = {
    "Name of standard or process": {
        "field_name": "name",
        "resolution_method": "combine",
        "data_type": "str",
    },
    "Conformity": {
        "field_name": "conformity",
        "resolution_method": "choice",
        "data_type": choices.FullNoPartial,
    },
    "Process and standards - Description": {
        "field_name": "description",
        "resolution_method": "combine",
        "data_type": "str",
    },
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


# Links have been done differently because the dictionary key is duplicated
all_headers = (
    list(key for key in evaluation_headers.keys())
    + list(key for key in outcome_measure_headers.keys())
    + list(key for key in other_measure_headers.keys())
    + list(key for key in grant_headers.keys())
    + [list(entry.keys())[0] for entry in links_headers]
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
    """
    Downloads the file to the data directory
    Args:
        url: The url given in the command to download the CSV from

    Returns:
        A filepath that points to the downloaded file
    """
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
    """
    Gets the headers from the given file
    Args:
        filename: The given filename to read from

    Returns:
        A list of headers from the given CSV
    """
    with open(filename, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        headers = [header for header in headers if header != ""]
    return headers


def get_evaluation_ids(data, headers):
    """
    Gets the unique and sorted id's of evaluations in the data
    Args:
        data: The data to get the id's from
        headers: The list of headers to find the Evaluation ID in

    Returns:
        A sorted list of unique id's relating to evaluations
    """
    unique_ids = set()
    column_index = headers.index("Evaluation ID")
    for row in data:
        id_value = row[column_index]
        if id_value:
            unique_ids.add(id_value)
    return sorted(unique_ids)


def get_evaluation_report_ids(data, headers):
    """
    Gets the unique and sorted id's of reports in a given evaluation
    Args:
        data: The data to get the id's from
        headers: The list of headers to find the Report ID in

    Returns:
        A sorted list of unique id's relating to reports of an evaluation
    """
    unique_ids = set()
    column_index = headers.index("Report ID")
    for row in data:
        id_value = row[column_index]
        if id_value:
            unique_ids.add(id_value)
    return sorted(unique_ids)


def get_data_rows(filename):
    """
    Takes in a filename and returns the rows of that CSV
    Args:
        filename: The filename to take rows from

    Returns:
        A list of rows that contain all the data of the given CSV
    """
    data = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        _ = next(reader)
        for row in reader:
            data.append(row)
        return data


def get_evaluation_rows_for_id(unique_id, rows, headers):
    """
    Gets the rows of data that relate to the given evaluation_id
    Args:
        unique_id: The evaluation to get rows for
        rows: All rows to take from
        headers: A list of headers to find the evaluation_id in

    Returns:
        A list of rows that match the given evaluation_id
    """
    column_index = headers.index("Evaluation ID")
    matching_rows = [row for row in rows if row[column_index] == unique_id]
    return matching_rows


def get_values_from_rows_for_header(rows, header, headers, report_id=None):
    """
    Gets all the values related to the given header, if a report_id is provided then only rows for that report are given. This is used to related items such as interventions
    Args:
        rows: The rows that relate to the evaluation record
        header: The required header
        headers: The headers from the CSV
        report_id: (optional) The report_id to get rows for

    Returns:
        A list of allowed values for this header
    """
    if report_id:
        report_id_index = headers.index("Report ID")
        values_of_header_rows = [row[headers.index(header)] for row in rows if row[report_id_index] == report_id]
    else:
        values_of_header_rows = [row[headers.index(header)] for row in rows]

    # Remove empty, unwanted and duplicate values
    allowed_values = []
    for value in values_of_header_rows:
        contains_disallowed = False
        for disallowed in disallowed_row_values:
            if disallowed in value.lower() or value.lower().strip().rstrip(".") == "" or value is None:
                contains_disallowed = True
                break
        if not contains_disallowed:
            allowed_values.append(value)
    return list(set(allowed_values))


def handle_simple_field(model, header_entry, values_of_header_rows):
    """
    Handles the setting of a simple field based on the field type taken from the header entry, either str or int, as well as the resolution method, either combine or single
    Args:
        model: The model to save changes to
        header_entry: The header entry that contains the information for this field
        values_of_header_rows: The values of the rows for this record
    """
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

        try:
            setattr(model, header_entry["field_name"], value)
            model.save()
        except (ValueError, DataError):
            print(
                f"Could not assign value {value} to {header_entry['field_name']}. This is likely because the value is too long for the field."
            )  # noqa: T201
            max_length = model._meta.get_field(header_entry["field_name"]).max_length
            setattr(model, header_entry["field_name"], value[: max_length - 1])
            model.save()
        except ValidationError:
            print(
                f"Could not assign value {value} to {header_entry['field_name']}. This is likely because the value is the wrong type."
            )  # noqa: T201
            pass


def handle_derived_evaluation_fields(evaluation, rows, headers):
    """
    Handles fields that need to be calculated or are derived from multiple columns such as evaluation type
    Args:
        evaluation: The evaluation to save changes to
        rows: The rows that contain the data for the evaluation
        headers: The headers from the file, used to ascertain which column in each row contains the relevant data
    """
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
    if process_evaluation_row_values_no < process_evaluation_row_values_yes:
        evaluation_types.append(choices.EvaluationTypeOptions.PROCESS.value)

    impact_evaluation_row_values = get_values_from_rows_for_header(rows, derived_fields["impact_evaluation"], headers)
    impact_evaluation_row_values_yes = sum(
        1 for row_value in impact_evaluation_row_values if row_value.lower() in positive_row_values
    )
    impact_evaluation_row_values_no = sum(
        1 for row_value in impact_evaluation_row_values if row_value.lower() in negative_row_values
    )
    if impact_evaluation_row_values_no < impact_evaluation_row_values_yes:
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
    if economic_evaluation_row_values_no < economic_evaluation_row_values_yes:
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

    # Set sample_size_details to any values that don't match options of sample_size
    sample_size_values = get_values_from_rows_for_header(rows, derived_fields["sample_size_details"], headers)
    sample_size_values_text = [sample_size for sample_size in sample_size_values if not sample_size.isdigit()]
    sample_size_details = ". ".join(s.strip().rstrip(".") for s in sample_size_values_text)
    if sample_size_details:
        setattr(evaluation, "sample_size_details", sample_size_details + ".")
    evaluation.save()


def handle_single_choice_field(model, header_entry, values_of_header_rows):
    """
    Handles the selecting of a single choice field based on either choices or from choice maps declared at the top of this script
    Args:
        model: The model to save changes to
        header_entry: The header entry that contains the information for this field
        values_of_header_rows: The values of the rows for this record
    """
    if values_of_header_rows:
        most_chosen_choice = max(set(values_of_header_rows), key=values_of_header_rows.count)
        most_chosen_choice = most_chosen_choice.rstrip(".")
        item_choices = header_entry["data_type"]
        selected_choice = [choice.name for choice in item_choices if choice.label.lower() == most_chosen_choice.lower()]
        if selected_choice:
            value = selected_choice[0]
            setattr(model, header_entry["field_name"], value)
            model.save()
        else:
            choices_support_other = supports_other[item_choices] or False
            if choices_support_other:
                value = "OTHER"
                setattr(model, header_entry["field_name"], value)
                model.save()
                try:
                    other_value = ". ".join(s.strip().rstrip(".") for s in values_of_header_rows) + "."
                    setattr(model, f"{header_entry['field_name']}_other", other_value)
                    model.save()
                except (ValueError, DataError):
                    other_value = ". ".join(s.strip().rstrip(".") for s in values_of_header_rows) + "."
                    print(
                        f"Could not assign value {other_value} to {header_entry['field_name']}_other. This is likely because the value is too long for the field. The value has been trimmed to fit."
                    )  # noqa: T201
                    max_length = model._meta.get_field(f"{header_entry['field_name']}_other").max_length
                    setattr(model, f"{header_entry['field_name']}_other", other_value[: max_length - 1])
                    model.save()
                except ValidationError:
                    print(
                        f"Could not assign to {header_entry['field_name']}_other. This is likely because the value is the wrong type."
                    )  # noqa: T201
                    pass


def handle_multiple_choice_field(model, header_entry, values_of_header_rows):
    """
    Handles the selecting of a multiple choice field based on either choices or from choice maps declared at the top of this script
    Args:
        model: The model to save changes to
        header_entry: The header entry that contains the information for this field
        values_of_header_rows: The values of the rows for this record
    """
    if values_of_header_rows:
        item_choices = header_entry["data_type"]
        lower_values_of_header_rows = [row_value.lower().strip().rstrip(".") for row_value in values_of_header_rows]
        present_choices = [
            choice.name for choice in item_choices if choice.label.lower() in lower_values_of_header_rows
        ]
        not_present_choices = [
            lower_value_of_header_rows
            for lower_value_of_header_rows in lower_values_of_header_rows
            if lower_value_of_header_rows not in [item_choice.label for item_choice in item_choices]
        ]
        if present_choices:
            setattr(model, header_entry["field_name"], present_choices)
            model.save()

        choices_support_other = supports_other[item_choices] or False
        if choices_support_other:
            try:
                model._meta.get_field(f"{header_entry['field_name']}_other")
                if not_present_choices:
                    if "OTHER" not in present_choices:
                        present_choices.append("OTHER")
                        setattr(model, header_entry["field_name"], present_choices)
                        model.save()
                    try:
                        other_value = ". ".join(s.strip().rstrip(".") for s in not_present_choices) + "."
                        setattr(model, f"{header_entry['field_name']}_other", other_value)
                        model.save()
                    except (ValueError, DataError):
                        other_value = ". ".join(s.strip().rstrip(".") for s in not_present_choices) + "."
                        print(
                            f"Could not assign value {other_value} to {header_entry['field_name']}_other. This is likely because the value is too long for the field. The value has been trimmed to fit."
                        )  # noqa: T201
                        max_length = model._meta.get_field(f"{header_entry['field_name']}_other").max_length
                        setattr(model, f"{header_entry['field_name']}_other", other_value[: max_length - 1])
                        model.save()
                    except ValidationError:
                        print(
                            f"Could not assign to {header_entry['field_name']}_other. This is likely because the value is the wrong type."
                        )  # noqa: T201
                        pass
            except FieldDoesNotExist:
                pass


def transform_and_create_from_rows(unique_row_id, rows, headers):
    """
    Handles each evaluation record by creating each relevant object individually and handling each column through the use of handle_simple_field, handle_single_choice_field and handle_multiple_choice_field
    Args:
        unique_row_id: The ID from the CSV of the evaluation data to prevent duplicates
        rows: The rows of data to handle for this evaluation
        headers: The headers from the files first row, used to match column data with headers
    """
    evaluation = models.Evaluation.objects.create()
    evaluation.visibility = "PUBLIC"
    evaluation.rsm_id = unique_row_id
    evaluation.save()

    evaluation_report_ids = get_evaluation_report_ids(rows, headers)

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

    # Intervention headers
    for evaluation_report_id in evaluation_report_ids:
        intervention = models.Intervention()
        intervention.evaluation = evaluation
        for header in headers:
            if header in intervention_headers:
                header_entry = intervention_headers[header]
                values_of_header_rows = get_values_from_rows_for_header(rows, header, headers, evaluation_report_id)
                if header_entry["data_type"] in (
                    "str",
                    "int",
                ):
                    handle_simple_field(intervention, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "choice":
                    handle_single_choice_field(intervention, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "multiple_choice":
                    handle_multiple_choice_field(intervention, header_entry, values_of_header_rows)

    # Links headers
    for evaluation_report_id in evaluation_report_ids:
        link = models.LinkOtherService()
        link.evaluation = evaluation
        for header in headers:
            # Looping link entries because two fields in links are being set by one csv field
            for entry in links_headers:
                if header in entry:
                    header_entry = entry[header]
                    values_of_header_rows = get_values_from_rows_for_header(rows, header, headers, evaluation_report_id)
                    if header_entry["data_type"] in (
                        "str",
                        "int",
                    ):
                        handle_simple_field(link, header_entry, values_of_header_rows)
                    elif header_entry["resolution_method"] == "choice":
                        handle_single_choice_field(link, header_entry, values_of_header_rows)
                    elif header_entry["resolution_method"] == "multiple_choice":
                        handle_multiple_choice_field(link, header_entry, values_of_header_rows)

    # Outcome measures headers
    for evaluation_report_id in evaluation_report_ids:
        outcome_measure = models.OutcomeMeasure()
        outcome_measure.evaluation = evaluation
        for header in headers:
            if header in outcome_measure_headers:
                header_entry = outcome_measure_headers[header]
                values_of_header_rows = get_values_from_rows_for_header(rows, header, headers, evaluation_report_id)
                if header_entry["data_type"] in (
                    "str",
                    "int",
                ):
                    handle_simple_field(outcome_measure, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "choice":
                    handle_single_choice_field(outcome_measure, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "multiple_choice":
                    handle_multiple_choice_field(outcome_measure, header_entry, values_of_header_rows)

    # Other measures headers
    for evaluation_report_id in evaluation_report_ids:
        other_measure = models.OtherMeasure()
        other_measure.evaluation = evaluation
        for header in headers:
            if header in other_measure_headers:
                header_entry = other_measure_headers[header]
                values_of_header_rows = get_values_from_rows_for_header(rows, header, headers, evaluation_report_id)
                if header_entry["data_type"] in (
                    "str",
                    "int",
                ):
                    handle_simple_field(other_measure, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "choice":
                    handle_single_choice_field(other_measure, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "multiple_choice":
                    handle_multiple_choice_field(other_measure, header_entry, values_of_header_rows)

    # Costs headers
    for evaluation_report_id in evaluation_report_ids:
        cost = models.EvaluationCost()
        cost.evaluation = evaluation
        for header in headers:
            if header in evaluation_cost_headers:
                header_entry = evaluation_cost_headers[header]
                values_of_header_rows = get_values_from_rows_for_header(rows, header, headers, evaluation_report_id)
                if header_entry["data_type"] in (
                    "str",
                    "int",
                ):
                    handle_simple_field(cost, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "choice":
                    handle_single_choice_field(cost, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "multiple_choice":
                    handle_multiple_choice_field(cost, header_entry, values_of_header_rows)

    # Processes and standards headers
    for evaluation_report_id in evaluation_report_ids:
        process_standard = models.ProcessStandard()
        process_standard.evaluation = evaluation
        for header in headers:
            if header in processes_and_standards_headers:
                header_entry = processes_and_standards_headers[header]
                values_of_header_rows = get_values_from_rows_for_header(rows, header, headers, evaluation_report_id)
                if header_entry["data_type"] in (
                    "str",
                    "int",
                ):
                    handle_simple_field(process_standard, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "choice":
                    handle_single_choice_field(process_standard, header_entry, values_of_header_rows)
                elif header_entry["resolution_method"] == "multiple_choice":
                    handle_multiple_choice_field(process_standard, header_entry, values_of_header_rows)

    # Derived evaluation headers
    handle_derived_evaluation_fields(evaluation, rows, headers)

    print(f"Evaluation uploaded. Title: {evaluation.title or 'No title found'}. ID: {evaluation.id}")  # noqa: T201

    # TODO: Organisations, costs, time points, figure out impact_interpretation_type data type?


def import_and_upload_evaluations(url):
    filename = save_url_to_data_dir(url)
    headers = get_sheet_headers(filename)
    rows = get_data_rows(filename)

    existing_evaluation_ids = [str(int(item.rsm_id)) for item in models.Evaluation.objects.filter(rsm_id__isnull=False)]
    print(f"{len(existing_evaluation_ids)} already imported records found")  # noqa: T201

    unique_row_ids = get_evaluation_ids(rows, headers)
    print(f"{len(unique_row_ids)} records found in the uploaded document")  # noqa: T201

    unique_and_non_duplicate_row_ids = [
        unique_row_id for unique_row_id in unique_row_ids if unique_row_id not in existing_evaluation_ids
    ]
    print(
        f"{len(unique_row_ids) - len(unique_and_non_duplicate_row_ids)} duplicates found. {len(unique_and_non_duplicate_row_ids)} new records to be imported"
    )  # noqa: T201

    for unique_row_id in unique_and_non_duplicate_row_ids:
        rows_for_id = get_evaluation_rows_for_id(unique_row_id, rows, headers)
        transform_and_create_from_rows(unique_row_id, rows_for_id, headers)
