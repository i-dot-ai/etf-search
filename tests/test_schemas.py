from datetime import date

from marshmallow import Schema, ValidationError
from nose.tools import with_setup

from eva_reg.evaluation import choices, models, schemas

from .utils import with_authenticated_client


class MadeUpSchema(Schema):
    date = schemas.DateAndBlankField(allow_none=True)
    choice_field_one = schemas.make_choice_field(max_len=3, values=choices.YesNo.values, allow_none=True)
    choice_field_two = schemas.make_choice_field(max_len=3, values=choices.YesNo.values, allow_none=False)


def test_date_and_blank_field():
    schema = MadeUpSchema()
    deserialized_obj = schema.load({"date": "2022-11-13"})
    assert deserialized_obj["date"] == date(2022, 11, 13)
    deserialized_obj = schema.load({"date": ""})
    assert deserialized_obj["date"] is None
    deserialized_obj = schema.load({"date": None})
    assert deserialized_obj["date"] is None


# Might not always want schemas to match, but we do for now
def check_schema_model_match_fields(model_name, schema_name, related_fields_to_ignore={}):
    model = getattr(models, model_name)
    schema = getattr(schemas, schema_name)
    model_field_names = {f.name for f in model._meta.get_fields()}
    model_field_names_to_include = model_field_names.difference(related_fields_to_ignore)
    schema_field_names = set(schema._declared_fields.keys())
    assert schema_field_names == model_field_names_to_include, model_field_names_to_include.difference(
        schema_field_names
    )


def test_evaluation_schema_has_relevant_fields():
    check_schema_model_match_fields(model_name="Evaluation", schema_name="EvaluationSchema")


def test_intervention_schema_has_relevant_fields():
    check_schema_model_match_fields(model_name="Intervention", schema_name="InterventionSchema")


def test_outcome_measure_schema_has_relevant_fields():
    check_schema_model_match_fields(model_name="OutcomeMeasure", schema_name="OutcomeMeasureSchema")


def test_other_measure_schema_has_relevant_fields():
    check_schema_model_match_fields(model_name="OtherMeasure", schema_name="OtherMeasureSchema")


def test_process_evaluation_method_schema_has_relevant_fields():
    check_schema_model_match_fields(model_name="ProcessEvaluationMethod", schema_name="ProcessEvaluationMethodSchema")


def test_process_evaluation_aspect_schema_has_relevant_fields():
    check_schema_model_match_fields(model_name="ProcessEvaluationAspect", schema_name="ProcessEvaluationAspectSchema")


def setup_evaluation():
    user, _ = models.User.objects.get_or_create(email="mrs.tiggywinkle@cabinetoffice.gov.uk")
    user.save()
    new_eval = models.Evaluation(title="Test evaluation schemas")
    new_eval.save()
    # TODO - add more fields
    new_eval.users.add(user)
    new_eval.save()
    model_names = ["OutcomeMeasure", "OtherMeasure", "Intervention"]
    for name in model_names:
        model = getattr(models, name)
        for i in range(3):
            new_obj = model(name=f"New obj {i}", evaluation=new_eval)
            new_obj.save()


def teardown_evaluation():
    evaluation = models.Evaluation.objects.get(title="Test evaluation schemas")
    evaluation.delete()
    user = models.User.objects.get(email="mrs.tiggywinkle@cabinetoffice.gov.uk")
    user.delete()


@with_setup(setup_evaluation, teardown_evaluation)
@with_authenticated_client
def test_evaluation_schema_dump(client):
    evaluation_schema = schemas.EvaluationSchema()
    evaluation = models.Evaluation.objects.get(title="Test evaluation schemas")
    serialized_evaluation = evaluation_schema.dump(evaluation)
    assert serialized_evaluation


def test_values_in_choices():
    acceptable_choices = ["A", "B", "C"]
    valid_data1 = ["A"]
    valid_data2 = []
    invalid_data = ["A", "D"]
    values_in_choices = schemas.make_values_in_choices(acceptable_choices)
    assert not values_in_choices(valid_data1)
    assert not values_in_choices(valid_data2)
    error_message = ""
    expected_error_message = "All values in list should be one of: ['A', 'B', 'C']"
    try:
        values_in_choices(invalid_data)
    except ValidationError as e:
        error_message = e.messages[0]
    assert error_message == expected_error_message, error_message


def test_evaluation_schema():
    evaluation_schema = schemas.EvaluationSchema()
    # TODO - should really have more fields, and nested fields!
    valid_data = {
        "title": "My first evaluation",
        "brief_description": "Hello, I am a brief description",
        "visibility": choices.EvaluationVisibility.DRAFT.value,
        "evaluation_type": [choices.EvaluationTypeOptions.PROCESS, choices.EvaluationTypeOptions.IMPACT],
        "ethics_committee_approval": "YES",
        "impact_design_name": [choices.ImpactEvalDesign.BAYESIAN_UPDATING, choices.ImpactEvalDesign.OTHER],
    }
    invalid_evaluation_type = {
        "title": "Title",
        "visibility": choices.EvaluationVisibility.CIVIL_SERVICE.value,
        "evaluation_type": ["STAR"],
    }
    assert evaluation_schema.load(valid_data)
    error_message = ""
    try:
        evaluation_schema.load(invalid_evaluation_type)
    except ValidationError as e:
        error_message = e.messages["evaluation_type"][0]
    assert error_message == "All values in list should be one of: ('IMPACT', 'PROCESS', 'ECONOMIC', 'OTHER')"


def test_user_schema():
    user_schema = schemas.UserSchema()
    error_message = ""
    try:
        user_schema.load({"email": "invalid@example.org"})
    except ValidationError as e:
        error_message = e.messages["email"][0]
    assert error_message == "This should be a valid Civil Service email", error_message
    try:
        user_schema.load({"email": "p"})
    except ValidationError as e:
        error_message = e.messages["email"][0]
    assert error_message == "This should be a valid Civil Service email", error_message


def test_make_choice_field():
    schema = MadeUpSchema()
    deserialized_obj = schema.load({"date": "2022-11-13", "choice_field_one": "", "choice_field_two": "YES"})
    assert deserialized_obj["date"] == date(2022, 11, 13)
    assert deserialized_obj["choice_field_one"] == ""
    assert deserialized_obj["choice_field_two"] == "YES"
    try:
        deserialized_obj = schema.load({"date": "2022-11-13", "choice_field_one": "NO", "choice_field_two": ""})
    except ValidationError as e:
        error_message = e.messages["choice_field_two"][0]
        assert "Must be one of: YES, NO." in error_message, error_message
    try:
        deserialized_obj = schema.load({"date": "2022-11-13", "choice_field_one": "bob", "choice_field_two": "NO"})
    except ValidationError as e:
        error_message = e.messages["choice_field_one"][0]
        assert "Must be one of: YES, NO." in error_message, error_message
