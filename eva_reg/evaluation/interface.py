import marshmallow

from . import models, schemas
from .utils import Entity, Facade, register_event, with_schema


class CreateEvaluationSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()


class GetEvaluationSchema(marshmallow.Schema):
    evaluation_id = marshmallow.fields.UUID()


class UpdateEvaluationSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()
    evaluation_id = marshmallow.fields.UUID()
    data = marshmallow.fields.Nested(schemas.EvaluationSchema)


class UpdateEvaluationVisibilitySchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()
    evaluation_id = marshmallow.fields.UUID()
    page_name = marshmallow.fields.Str()
    status = marshmallow.fields.Str()


class AddUserToEvaluationSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()  # User making request
    evaluation_id = marshmallow.fields.UUID()
    user_to_add_data = marshmallow.fields.Nested(schemas.UserSchema)  # User being added


class AddUserToEvaluationResponseSchema(marshmallow.Schema):
    evaluation_id = marshmallow.fields.UUID()
    user_added_id = marshmallow.fields.UUID()
    is_new_user = marshmallow.fields.Boolean()


class RemoveEvaluationUserSchema(marshmallow.Schema):
    user_id = marshmallow.fields.UUID()
    evaluation_id = marshmallow.fields.UUID()
    user_to_remove_id = marshmallow.fields.UUID()


class Evaluation(Entity):
    @with_schema(load=CreateEvaluationSchema, dump=schemas.EvaluationSchema)
    @register_event("Evaluation created")
    def create(self, user_id):
        user = models.User.objects.get(id=user_id)
        evaluation = models.Evaluation()
        evaluation.save()
        evaluation.users.add(user)
        evaluation.save()
        return evaluation

    @with_schema(load=GetEvaluationSchema, dump=schemas.EvaluationSchema)
    def get(self, evaluation_id):
        evaluation = models.Evaluation.objects.get(id=evaluation_id)
        return evaluation

    @with_schema(load=UpdateEvaluationSchema(partial=True), dump=schemas.EvaluationSchema)
    @register_event("Evaluation updated")
    def update(self, user_id, evaluation_id, data):
        evaluation = models.Evaluation.objects.get(id=evaluation_id, users__id=user_id)
        for key, value in data.items():
            setattr(evaluation, key, value)
        evaluation.save()
        return evaluation

    @with_schema(load=UpdateEvaluationVisibilitySchema, dump=schemas.EvaluationSchema)
    def update_page_status(self, user_id, evaluation_id, page_name, status):
        evaluation = models.Evaluation.objects.get(id=evaluation_id, users__id=user_id)
        evaluation.update_evaluation_page_status(page_name, status)
        evaluation.save()
        return evaluation

    @with_schema(load=AddUserToEvaluationSchema, dump=AddUserToEvaluationResponseSchema)
    @register_event("User added to evaluation")
    def add_user_to_evaluation(self, user_id, evaluation_id, user_to_add_data):
        evaluation = models.Evaluation.objects.get(id=evaluation_id)
        user_added, is_new_user = models.User.objects.update_or_create(
            email=user_to_add_data["email"], defaults=user_to_add_data
        )
        evaluation.users.add(user_added)
        output = {"evaluation_id": evaluation_id, "user_added_id": user_added.id, "is_new_user": is_new_user}
        return output

    @with_schema(load=RemoveEvaluationUserSchema, dump=schemas.UserSchema(many=True))
    @register_event("User removed from evaluation")
    def remove_user_from_evaluation(self, user_id, evaluation_id, user_to_remove_id):
        evaluation = models.Evaluation.objects.get(id=evaluation_id)
        user_to_remove = models.User.objects.get(id=user_to_remove_id)
        evaluation.users.remove(user_to_remove)
        return evaluation.users.all()


facade = Facade(evaluation=Evaluation())
