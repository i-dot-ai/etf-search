import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from eva_reg.evaluation.choices import EvaluationVisibility
from eva_reg.evaluation.models import Evaluation
from eva_reg.evaluation.schemas import EvaluationSchema
from eva_reg.evaluation.utils import restrict_to_permitted_evaluations


@login_required
def filter_evaluations_to_download(request):
    user = request.user
    qs = Evaluation.objects.all()
    restricted_evaluations = restrict_to_permitted_evaluations(user, qs)
    output_qs = Evaluation.objects.none()
    if "civil_service_only" in request.GET:
        civil_service_evals = restricted_evaluations.filter(visibility=EvaluationVisibility.CIVIL_SERVICE.value)
        output_qs = output_qs | civil_service_evals
    if "public" in request.GET:
        public_evals = restricted_evaluations.filter(visibility=EvaluationVisibility.PUBLIC.value)
        output_qs = output_qs | public_evals
    if "my_evaluations" in request.GET:
        user_evals = user.evaluations.all()
        output_qs = output_qs | user_evals
    return output_qs


@login_required
def download_json_view(request):
    evaluations_qs = filter_evaluations_to_download(request)
    evaluation_schema = EvaluationSchema()
    data = evaluation_schema.dumps(evaluations_qs, many=True)
    headers = {
        "Content-Type": "application/json",
        "Content-Disposition": "attachment; filename=evaluation-data.json",
    }
    response = HttpResponse(data, headers=headers)
    return response


@login_required
def download_csv_view(request):
    evaluations_qs = filter_evaluations_to_download(request)
    evaluation_schema = EvaluationSchema()
    data = evaluation_schema.dump(evaluations_qs, many=True)
    headers = {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=evaluation-data.csv",
    }
    response = HttpResponse(headers=headers)
    # TODO - do we want only selected fields, and in what order?
    fieldnames = []
    if data:
        fieldnames = list(data[0].keys())
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return response


@login_required
def download_page_view(request):
    if "json" in request.GET:
        return download_json_view(request)
    elif "csv" in request.GET:
        return download_csv_view(request)
    return render(request, "data-download.html", {"errors": {}, "data": {}})
