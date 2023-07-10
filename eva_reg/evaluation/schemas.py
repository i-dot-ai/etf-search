from marshmallow import Schema, ValidationError, fields, validate

from etf.evaluation.utils import is_civil_service_email

from . import choices


def make_values_in_choices(choices_values):
    def values_in_choices(list_values):
        for value in list_values:
            if value not in choices_values:
                raise ValidationError(f"All values in list should be one of: {choices_values}")

    return values_in_choices


def validate_email(email):
    if not is_civil_service_email(email):
        raise ValidationError("This should be a valid Civil Service email")
    return True


class DateAndBlankField(fields.Date):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            return super()._deserialize(value, attr, data, **kwargs)
        else:
            return None


class FloatAndBlankField(fields.Float):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            return super()._deserialize(value, attr, data, **kwargs)
        else:
            return None


class IntAndBlankField(fields.Int):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            return super()._deserialize(value, attr, data, **kwargs)
        else:
            return None


class SingleLineStr(fields.Str):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            single_line_value = " ".join(value.splitlines())
            if not value == single_line_value:
                raise ValidationError("Cannot contain linebreaks")
        return super()._deserialize(value, attr, data, **kwargs)


def validate_choice_and_length_or_none(values):
    def validator(value):
        if value != "" and not validate.OneOf(values):
            raise ValidationError(f"Value needs to be in {values} or None")

    return validator


def make_choice_field(max_len, values, allow_none=False, **kwargs):
    if allow_none:
        field = SingleLineStr(
            validate=validate.And(validate.Length(max=max_len), validate_choice_and_length_or_none(values)),
            allow_none=True,
            **kwargs,
        )
    else:
        field = SingleLineStr(validate=validate.And(validate.Length(max=max_len), validate.OneOf(values)), **kwargs)
    return field


def make_multi_choice_field(max_len, values):
    field = fields.Raw(validate=validate.And(validate.Length(max=max_len), make_values_in_choices(values)))
    return field


def is_non_neg_int_or_none(value):
    error = validate.ValidationError("Value should be a non-negative integer")
    if not isinstance(value, int):
        if not value:
            value = None
        else:
            raise error
    elif value < 0:
        raise error


class UserSchema(Schema):
    email = fields.Str(validate=validate_email)


class TimeStampedModelSchema(Schema):
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)


class EvaluationSchema(TimeStampedModelSchema):
    # TODO - add more validation esp. for choice fields, around dates
    users = fields.Function(lambda e: UserSchema(many=True).dump(e.users.all()))
    id = fields.UUID()
    title = SingleLineStr(required=True, validate=validate.Length(max=1024))
    brief_description = fields.Str()
    topics = make_multi_choice_field(max_len=64, values=choices.Topic.values)
    organisations = fields.Raw()
    visibility = make_choice_field(
        max_len=256, values=choices.EvaluationVisibility.values, default=choices.EvaluationVisibility.DRAFT.value
    )

    doi = fields.Str(validate=validate.Length(max=64))
    page_statuses = fields.Raw()

    # Options
    issue_description_option = make_choice_field(max_len=3, values=choices.YesNo.values, allow_none=True)
    ethics_option = make_choice_field(max_len=3, values=choices.YesNo.values, allow_none=True)
    grants_option = make_choice_field(max_len=3, values=choices.YesNo.values, allow_none=True)

    # Issue description
    issue_description = fields.Str()
    those_experiencing_issue = fields.Str()
    why_improvements_matter = fields.Str()
    who_improvements_matter_to = fields.Str()
    current_practice = fields.Str()
    issue_relevance = fields.Str()

    # Evaluation costs and budget
    costs = fields.Function(lambda e: EvaluationCostSchema(many=True, exclude=("evaluation",)).dump(e.costs.all()))

    # Documents
    documents = fields.Function(lambda e: DocumentSchema(many=True, exclude=("evaluation",)).dump(e.documents.all()))

    # Event dates
    event_dates = fields.Function(
        lambda e: EventDateSchema(many=True, exclude=("evaluation",)).dump(e.event_dates.all())
    )

    # Evaluation type
    evaluation_type = make_multi_choice_field(max_len=64, values=choices.EvaluationTypeOptions.values)
    evaluation_type_other = SingleLineStr(validate=validate.Length(max=256))

    # Studied population
    studied_population = fields.Str()
    eligibility_criteria = fields.Str()
    sample_size = IntAndBlankField(validate=is_non_neg_int_or_none, allow_none=True)
    sample_size_units = SingleLineStr(validate=validate.Length(max=256))
    sample_size_details = fields.Str()

    # Participant recruitment approach
    process_for_recruitment = fields.Str()
    recruitment_schedule = fields.Str()

    # Ethical considerations
    ethics_committee_approval = make_choice_field(max_len=3, values=choices.YesNo.values, allow_none=True)
    ethics_committee_details = fields.Str()
    ethical_state_given_existing_evidence_base = fields.Str()
    risks_to_participants = fields.Str()
    risks_to_study_team = fields.Str()
    participant_involvement = fields.Str()
    participant_information = fields.Str()
    participant_consent = fields.Str()
    participant_payment = fields.Str()
    confidentiality_and_personal_data = fields.Str()
    breaking_confidentiality = fields.Str()
    other_ethical_information = fields.Str()

    # Impact evaluation design

    impact_design_name = make_multi_choice_field(max_len=128, values=choices.ImpactEvalDesign.values)
    impact_design_name_other = SingleLineStr(validate=validate.Length(max=64))
    impact_design_justification = fields.Str()
    impact_design_description = fields.Str()
    impact_design_features = fields.Str()
    impact_design_equity = fields.Str()
    impact_design_assumptions = fields.Str()
    impact_design_approach_limitations = fields.Str()

    # Impact evaluation analysis
    impact_framework = make_choice_field(max_len=64, values=choices.ImpactFramework.values)
    impact_framework_other = SingleLineStr(validate=validate.Length(max=256))
    impact_basis = make_choice_field(max_len=64, values=choices.ImpactAnalysisBasis.values)
    impact_basis_other = SingleLineStr(validate=validate.Length(max=256))
    impact_analysis_set = fields.Str()
    impact_effect_measure_type = make_choice_field(max_len=64, values=choices.ImpactMeasureType.values)
    impact_effect_measure_type_other = SingleLineStr(validate=validate.Length(max=256))
    impact_primary_effect_size_measure = fields.Str()
    impact_effect_measure_interval = make_choice_field(max_len=64, values=choices.ImpactMeasureInterval.values)
    impact_effect_measure_interval_other = SingleLineStr(validate=validate.Length(max=256))
    impact_primary_effect_size_desc = fields.Str()
    impact_interpretation_type = make_choice_field(max_len=64, values=choices.ImpactInterpretationType.values)
    impact_interpretation_type_other = SingleLineStr(validate=validate.Length(max=256))
    impact_sensitivity_analysis = fields.Str()
    impact_subgroup_analysis = fields.Str()
    impact_missing_data_handling = fields.Str()
    impact_fidelity = make_choice_field(max_len=10, values=choices.YesNo.values, allow_none=True)
    impact_description_planned_analysis = fields.Str()

    # Process evaluation aspects
    process_evaluation_aspects = fields.Function(
        lambda e: ProcessEvaluationAspectSchema(many=True, exclude=("evaluation",)).dump(
            e.process_evaluation_aspects.all()
        )
    )

    # Process evaluation method
    process_evaluation_methods = fields.Function(
        lambda e: ProcessEvaluationMethodSchema(many=True, exclude=("evaluation",)).dump(
            e.process_evaluation_methods.all()
        )
    )

    # Economic evaluation design
    economic_type = make_choice_field(max_len=256, values=choices.EconomicEvaluationType.values)
    perspective_costs = fields.Str()
    perspective_benefits = fields.Str()
    monetisation_approaches = fields.Str()
    economic_design_details = fields.Str()

    # Economic evaluation analysis
    economic_analysis_description = fields.Str()

    # Other evaluation design
    other_design_type = fields.Str()
    other_design_details = fields.Str()

    # Other evaluation analysis
    other_analysis_description = fields.Str()

    # Interventions
    interventions = fields.Function(
        lambda e: InterventionSchema(many=True, exclude=("evaluation",)).dump(e.interventions.all())
    )

    # Outcome measures
    outcome_measures = fields.Function(
        lambda e: OutcomeMeasureSchema(many=True, exclude=("evaluation",)).dump(e.outcome_measures.all())
    )

    # Other measurement
    other_measures = fields.Function(
        lambda e: OtherMeasureSchema(many=True, exclude=("evaluation",)).dump(e.other_measures.all())
    )

    # Impact evaluation findings
    impact_comparison = fields.Str()
    impact_outcome = fields.Str()
    impact_interpretation = make_choice_field(max_len=256, values=choices.ImpactEvalInterpretation.values)
    impact_interpretation_other = SingleLineStr(validate=validate.Length(max=256))
    impact_point_estimate_diff = fields.Str()
    impact_lower_uncertainty = fields.Str()
    impact_upper_uncertainty = fields.Str()
    impact_summary_findings = fields.Str()
    impact_findings = fields.Str()

    # Economic evaluation findings
    economic_summary_findings = fields.Str()
    economic_findings = fields.Str()

    # Process evaluation findings
    process_summary_findings = fields.Str()
    process_findings = fields.Str()

    # Other evaluation findings
    other_summary_findings = fields.Str()
    other_findings = fields.Str()

    # Processes and standards
    process_standards = fields.Function(
        lambda e: ProcessStandardSchema(many=True, exclude=("evaluation",)).dump(e.process_standards.all())
    )

    # Grants
    grants = fields.Function(lambda e: GrantSchema(many=True, exclude=("evaluation",)).dump(e.grants.all()))

    # Links and IDs
    link_other_services = fields.Function(
        lambda e: LinkOtherServiceSchema(many=True, exclude=("evaluation",)).dump(e.link_other_services.all())
    )

    search_text = fields.Str()
    rsm_id = fields.Float()


class InterventionSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema())
    id = fields.UUID(dump_only=True)
    name = SingleLineStr(validate=validate.Length(max=1024))
    brief_description = fields.Str()
    rationale = fields.Str()
    materials_used = fields.Str()
    procedures = fields.Str()
    provider_description = fields.Str()
    modes_of_delivery = fields.Str()
    location = fields.Str()
    frequency_of_delivery = fields.Str()
    tailoring = fields.Str()
    fidelity = fields.Str()
    resource_requirements = fields.Str()
    geographical_information = fields.Str()


class OutcomeMeasureSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    name = SingleLineStr(validate=validate.Length(max=256))
    primary_or_secondary = make_choice_field(max_len=10, values=choices.OutcomeType.values)
    direct_or_surrogate = make_choice_field(max_len=10, values=choices.OutcomeMeasure.values)
    measure_type = make_choice_field(max_len=256, values=choices.MeasureType.values)
    measure_type_other = SingleLineStr(validate=validate.Length(max=256))
    description = fields.Str()
    collection_process = fields.Str()
    timepoint = fields.Str()
    minimum_difference = fields.Str()
    relevance = fields.Str()


class OtherMeasureSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    name = SingleLineStr(validate=validate.Length(max=256))
    measure_type = make_choice_field(max_len=256, values=choices.MeasureType.values)
    measure_type_other = fields.Str(validate=validate.Length(max=256))
    description = fields.Str()
    collection_process = fields.Str()


class ProcessStandardSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    name = SingleLineStr(validate=validate.Length(max=1024))
    conformity = make_choice_field(max_len=10, values=choices.FullNoPartial.values)
    description = fields.Str()


class GrantSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    name_of_grant = SingleLineStr(validate=validate.Length(max=1024))
    grant_number = SingleLineStr(validate=validate.Length(max=1024))
    grant_details = fields.Str()


class DocumentSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    title = SingleLineStr(validate=validate.Length(max=256))
    url = fields.Url(validate=validate.Length(max=512))
    description = fields.Str()
    document_types = make_multi_choice_field(max_len=64, values=choices.DocumentType.values)
    document_type_other = SingleLineStr(validate=validate.Length(max=256))


class EventDateSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    event_date_name = make_choice_field(max_len=256, values=choices.EventDateOption.values)
    event_date_name_other = SingleLineStr(validate=validate.Length(max=256))
    date = DateAndBlankField()
    event_date_type = make_choice_field(max_len=10, values=choices.EventDateType.values)


class LinkOtherServiceSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    name_of_service = SingleLineStr(validate=validate.Length(max=256))
    link_or_identifier = SingleLineStr(validate=validate.Length(max=256))


class EvaluationCostSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    item_name = SingleLineStr()
    description = fields.Str()
    item_cost = FloatAndBlankField()
    earliest_spend_date = DateAndBlankField()
    latest_spend_date = DateAndBlankField()


class ProcessEvaluationDesignAspectsSchema(Schema):  # Not the same as model
    aspect_name = make_multi_choice_field(max_len=256, values=choices.ProcessEvaluationAspects.values)
    aspect_name_other = SingleLineStr(validate=validate.Length(max=256))


class ProcessEvaluationMethodSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    method_name = make_choice_field(max_len=256, values=choices.ProcessEvaluationMethods.values)
    method_name_other = SingleLineStr(validate=validate.Length(max=256))
    more_information = fields.Str()
    aspects_measured = make_multi_choice_field(max_len=256, values=choices.ProcessEvaluationAspects.values)


class ProcessEvaluationAspectSchema(TimeStampedModelSchema):
    evaluation = fields.Nested(EvaluationSchema)
    id = fields.UUID(dump_only=True)
    aspect_name = make_choice_field(max_len=256, values=choices.ProcessEvaluationAspects.values)
    aspect_name_other = SingleLineStr(validate=validate.Length(max=256))
    summary_findings = fields.Str()
    findings = fields.Str()
