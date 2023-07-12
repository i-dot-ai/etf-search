from . import enums, utils


class EvaluationTypeOptions(utils.Choices):
    IMPACT = "Impact evaluation"
    PROCESS = "Process evaluation"
    ECONOMIC = "Economic evaluation"
    OTHER = "Other"


class OutcomeType(utils.Choices):
    PRIMARY = "Primary"
    SECONDARY = "Secondary"


class OutcomeMeasure(utils.Choices):
    DIRECT = "Direct"
    SURROGATE = "Surrogate"


class YesNo(utils.Choices):
    YES = "Yes"
    NO = "No"


class YesNoPartial(utils.Choices):
    YES = "Yes"
    NO = "No"
    PARTIAL = "Partial"


class FullNoPartial(utils.Choices):
    FULL = "Full"
    PARTIAL = "Partial"
    NO = "No"


class MeasureType(utils.Choices):
    CONTINUOUS = "Continuous"
    DISCRETE = "Discrete"
    BINARY = "Binary"
    ORDINAL = "Ordinal"
    NOMINAL = "Nominal"
    OTHER = "Other"


# TODO - to improve
class Topic(utils.Choices):
    BREXIT = "Brexit"
    BUSINESS_AND_INDUSTRY = "Business and industry"
    CORONAVIRUS = "Coronavirus"
    CORPORATE_INFORMATION = "Corporate information"
    CRIME_JUSTICE_AND_LAW = "Crime, justice and law"
    DEFENCE_AND_ARMED_FORCES = "Defence and armed forces"
    EDUCATION_TRAINING_AND_SKILLS = "Education, training and skills"
    ENTERING_AND_STAYING_IN_THE_UK = "Entering and staying in the UK"
    ENVIRONMENT = "Environment"
    GOING_AND_BEING_ABROAD = "Going and being abroad"
    GOVERNMENT = "Government"
    HEALTH_AND_SOCIAL_CARE = "Health and social care"
    HOUSING_LOCAL_AND_COMMUNITY = "Housing, local and community"
    INTERNATIONAL = "International"
    LIFE_CIRCUMSTANCES = "Life circumstances"
    MONEY = "Money"
    PARENTING_CHILDCARE_AND_CHILDRENS_SERVICES = "Parenting, childcare and children's services"
    REGIONAL_AND_LOCAL_GOVERNMENT = "Regional and local government"
    SOCIETY_AND_CULTURE = "Society and culture"
    TRANSPORT = "Transport"
    WELFARE = "Welfare"


class EvaluationVisibility(utils.Choices):
    DRAFT = "Draft"
    CIVIL_SERVICE = "Civil Service"
    PUBLIC = "Public"


class DocumentType(utils.Choices):
    SCOPING_REPORT = "Scoping report"
    FEASIBILITY_STUDY_REPORT = "Feasibility study report"
    STUDY_PROTOCOL = "Study protocol"
    ANALYSIS_PLAN = "Analysis plan"
    THEORY_OF_CHANGE = "Theory of change/Causal-chain map/Logic model"
    SUMMARY_INTERIM = "Summary interim results report"
    MAIN_INTERIM = "Main interim results report"
    SUMMARY_FINAL = "Summary final results report"
    MAIN_FINAL = "Main final results report"
    TECHNICAL_REPORT = "Technical report"
    DATASET = "Data set"
    ANALYSIS_CODE = "Analysis code"
    OTHER = "Other"


class EventDateOption(utils.Choices):
    EVALUATION_START = "Evaluation start"
    EVALUATION_END = "Evaluation end"
    FIRST_PARTICIPANT_RECRUITED = "First participant recruited"
    LAST_PARTICIPANT_RECRUITED = "Last participant recruited"
    INTERVENTION_START_DATE = "Intervention start date"
    INTERVENTION_END_DATE = "Intervention end date"
    INTERIM_DATA_EXTRACTION_DATE = "Interim data extraction date"
    INTERIM_DATA_ANALYSIS_START = "Interim data analysis start"
    INTERIM_DATA_ANALYSIS_END = "Interim data analysis end"
    PUBLICATION_INTERIM_RESULTS = "Publication of interim results"
    FINAL_DATA_EXTRACTION_DATE = "Final data extraction date"
    FINAL_DATA_ANALYSIS_START = "Final data analysis start"
    FINAL_DATA_ANALYSIS_END = "Final data analysis end"
    PUBLICATION_FINAL_RESULTS = "Publication of final results"
    OTHER = "Other"


class EventDateType(utils.Choices):
    INTENDED = "Intended"
    ACTUAL = "Actual"


class EconomicEvaluationType(utils.Choices):
    COST_MINIMISATION = "Cost minimisation"
    COST_EFFECTIVENESS_ANALYSIS = "Cost-effectiveness analysis"
    COST_BENEFIT_ANALYSIS = "Cost-benefit analysis"
    COST_UTILITY_ANALYSIS = "Cost-utility analysis"


# TODO - nested choices
class ImpactEvalInterpretation(utils.Choices):
    SUPERIORITY_SUPERIOR = "Superiority framework: Superior"
    SUPERIORITY_INFERIOR = "Superiority framework: Inferior"
    SUPERIORITY_INCONCLUSIVE = "Superiority framework: Inconclusive"
    NON_INFERIORITY_SUPERIOR = "Non-inferiority framework: Superior"
    NON_INFERIORITY_NON_INFERIOR = "Non-inferiority framework: Non-inferior"
    NON_INFERIORITY_INFERIOR = "Non-inferiority framework: Inferior"
    NON_INFERIORITY_INCONCLUSIVE = "Non-inferiority framework: Inconclusive"
    EQUIVALENCE_EQUIVALENT = "Equivalence framework: Equivalent"
    EQUIVALENCE_NON_EQUIVALENT = "Equivalence framework: Non-equivalent"
    EQUIVALENCE_NON_EQUIVALENT_SUPERIOR = "Equivalence framework: Non-equivalent (superior)"
    EQUIVALENCE_NON_EQUIVALENT_INFERIOR = "Equivalence framework: Non-equivalent (inferior)"
    EQUIVALENCE_NON_EQUIVALENT_INCONCLUSIVE = "Equivalence framework: Inconclusive"
    OTHER = "Other"


# TODO - nested choices
class ImpactEvalDesign(utils.Choices):
    RCT = "Experimental methods for impact evaluation: Randomised controlled trial (RCT)"
    CLUSTER_RCT = "Experimental methods for impact evaluation: Cluster randomised RCT"
    STEPPED_WEDGE_RCT = "Experimental methods for impact evaluation: Stepped wedge RCT"
    WAITLIST_RCT = "Experimental methods for impact evaluation: Wait-list RCT"
    PROPENSITY_SCORE_MATCHING = "Quasi-experimental methods for impact evaluation: Propensity score matching"
    TIMING_OF_EVENTS = "Quasi-experimental methods for impact evaluation: Timing of events"
    INTERRUPTED_TIME_SERIES_ANALYSIS = (
        "Quasi-experimental methods for impact evaluation: Interrupted time series analysis"
    )
    INSTRUMENTAL_VARIABLES = "Quasi-experimental methods for impact evaluation: Instrumental variables"
    SYNTHETIC_CONTROL_METHODS = "Quasi-experimental methods for impact evaluation: Synthetic control methods"
    DIFF_IN_DIFF = "Quasi-experimental methods for impact evaluation: Difference-in-difference"
    REGRESSION_DISCONTINUITY = "Quasi-experimental methods for impact evaluation: Regression discontinuity"
    QCA = "Theory-based methods for impact evaluation: Qualitative comparative analysis (QCA)"
    REALISE_EVALUATION = "Theory-based methods for impact evaluation: Realist evaluation"
    PROCESS_TRACING = "Theory-based methods for impact evaluation: Process tracing"
    CONSTRIBUTION_ANALYSIS = "Theory-based methods for impact evaluation: Contribution analysis"
    BAYESIAN_UPDATING = "Theory-based methods for impact evaluation: Bayesian updating"
    CONTRIBUTION_TRACING = "Theory-based methods for impact evaluation: Contribution tracing"
    MOST_SIGNIFICANT_CHANGE = "Theory-based methods for impact evaluation: Most significant change"
    OUTCOME_HARVESTING = "Theory-based methods for impact evaluation: Outcome harvesting"
    SIMULATION_MODELLING = "Theory-based methods for impact evaluation: Simulation modelling"
    INDIVIDUAL_INTERVIEWS = "Generic research methods used in both process and impact evaluation: Individual interviews"
    FOCUS_GROUPS = (
        "Generic research methods used in both process and impact evaluation: Focus groups or group interviews"
    )
    CASE_STUDIES = "Generic research methods used in both process and impact evaluation: Case studies"
    SURVEYS_AND_POLLING = "Generic research methods used in both process and impact evaluation: Surveys and polling"
    OUTPUT_OR_PERFORMANCE_MONITORING = (
        "Generic research methods used in both process and impact evaluation: Output or performance modelling"
    )
    QUALITATIVE_OBSERVATIONAL_STUDIES = (
        "Generic research methods used in both process and impact evaluation: Qualitative observational studies"
    )
    CONSULTATIVE_METHODS = (
        "Generic research methods used in both process and impact evaluation: Consultative/deliberative methods"
    )
    OTHER = "Other"


class ImpactFramework(utils.Choices):
    SUPERIORITY = "Superiority"
    NON_INFERIORITY = "Non-inferiority"
    EQUIVALENCE = "Equivalence"
    OTHER = "Other"


class ImpactAnalysisBasis(utils.Choices):
    INTENTION_TO_TREAT = "Intention-to-treat"
    PER_PROTOCOL = "Per-protocol"
    OTHER = "Other"


class ImpactMeasureInterval(utils.Choices):
    CONFIDENCE = "Confidence interval"
    BAYESIAN = "Bayesian credible interval"
    NONE = "None"
    OTHER = "Other"


class ImpactInterpretationType(utils.Choices):
    INTERVALS = "Interpretation of intervals"
    HYPOTHESIS = "Hypothesis testing"
    NONE = "None"
    OTHER = "Other"


class ImpactMeasureType(utils.Choices):
    ABSOLUTE = "Absolute measure"
    RELATIVE = "Relative measure"
    OTHER = "Other"


class ProcessEvaluationAspects(utils.Choices):
    IMPLEMENTATION = "Implementation feasibility"
    FIDELITY = "Fidelity"
    ACCEPTABILITY_TARGET_POPULATION = "Acceptability to target population"
    ACCEPTABILITY_IMPLEMENTERS = "Acceptability to implementers"
    PARTICIPATION = "Participation"
    PERCEPTION_OF_RELEVANCE = "Participants' perceptions of relevance of intervention"
    INTENTION_TO_USE = "Participants' intention to use (for example, knowledge gained from intervention)"
    IMPACT_INTERMEDIATE_OUTCOMES = "Impact on intermediate outcomes"
    QUALITATIVE_STUDY_CAUSAL_PROCESSES = "Qualitative study to explore causal processes"
    UNANTICIPATED_OUTCOMES = "Unanticipated outcomes (beneficial or adverse)"
    CONTEXT_IMPACT_IMPLEMENTATION = "Context: impact on implementation"
    CONTEXT_IMPACT_OUTCOMES = "Context: impact on outcomes"
    SUSTAINABILITY_OF_PROGRAMME = "Sustainability of the programme"
    EVALUATION_FEASIBILITY = "Evaluation feasibility"
    OTHER = "Other"


class ProcessEvaluationMethods(utils.Choices):
    INDIVIDUAL_INTERVIEWS = "Individual interviews"
    FOCUS_GROUPS = "Focus groups or group interviews"
    CASE_STUDIES = "Case studies"
    SURVEYS_AND_POLLING = "Surveys and polling"
    OUTPUT_OR_PERFORMANCE_MONITORING = "Output or performance modelling"
    QUALITATIVE_OBSERVATIONAL_STUDIES = "Qualitative observational studies"
    CONSULTATIVE_METHODS = "Consultative/deliberative methods"
    OTHER = "Other"


dropdown_choices = {
    "document_types": DocumentType.choices,
    "economic_type": EconomicEvaluationType.choices,
    "evaluation_type": EvaluationTypeOptions.choices,
    "event_date_name": EventDateOption.choices,
    "event_date_type": EventDateType.choices,
    "impact_design_name": ImpactEvalDesign.choices,
    "impact_framework": ImpactFramework.choices,
    "impact_basis": ImpactAnalysisBasis.choices,
    "impact_effect_measure_type": ImpactMeasureType.choices,
    "impact_effect_measure_interval": ImpactMeasureInterval.choices,
    "impact_interpretation": ImpactEvalInterpretation.choices,
    "impact_interpretation_type": ImpactInterpretationType.choices,
    "process_evaluation_aspect": ProcessEvaluationAspects.choices,
    "process_evaluation_method": ProcessEvaluationMethods.choices,
    "measure_type": MeasureType.choices,
    "organisations": enums.Organisation.choices,
    "topics": Topic.choices,
}


def get_db_values(choices):
    output = [x[0] for x in choices]
    return output


def get_display_name(db_name, choices_options):
    result = [choice["text"] for choice in choices_options if choice["value"] == db_name]
    if not result:
        return None
    return result[0]


def map_choice_or_other(input, choices_options, append_separator=False):
    """
    If value is from the list of choices, return the display value.
    Otherwise this is the specified value for the 'other' choice,
    and return this.
    """
    if not input:
        mapped_value = ""
    mapped_value = get_display_name(input, choices_options)
    if not mapped_value:
        mapped_value = input
    if append_separator:
        mapped_value = f"{mapped_value}{utils.SEPARATOR}"
    return mapped_value


def turn_list_to_display_values(db_list, choices_options):
    if not db_list:
        return []
    output_list = [map_choice_or_other(x, choices_options) for x in db_list]
    return output_list


def turn_choices_list_to_string(db_list, choices_options):
    display_list = turn_list_to_display_values(db_list, choices_options)
    output = utils.SEPARATOR.join(display_list)
    if output:
        output = f"{output}{utils.SEPARATOR}"
    return output


def map_other(pair, specified_other_description):
    if pair[0] == "OTHER":
        other_name = pair[1]
        full_other_name = f"{other_name} ({specified_other_description})"
        return ("OTHER", full_other_name)
    return pair


def restrict_choices(choices, values_to_restrict_to, specified_other=""):
    restricted = (choice for choice in choices if choice[0] in values_to_restrict_to)
    if specified_other and ("OTHER" in values_to_restrict_to):
        restricted = (map_other(x, specified_other) for x in restricted)
    return restricted
