from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from etf.evaluation import choices, enums, models

from .utils import check_evaluation_view_permission


@check_evaluation_view_permission
def evaluation_summary_overview_view(request, evaluation_id):
    return evaluation_summary_view(request, evaluation_id, "overview/evaluation-overview.html")


@check_evaluation_view_permission
def evaluation_measured_overview_view(request, evaluation_id):
    return evaluation_summary_view(request, evaluation_id, "overview/evaluation-overview-measured.html")


@check_evaluation_view_permission
def evaluation_design_overview_view(request, evaluation_id):
    return evaluation_summary_view(request, evaluation_id, "overview/evaluation-overview-design.html")


@check_evaluation_view_permission
def evaluation_analysis_overview_view(request, evaluation_id):
    return evaluation_summary_view(request, evaluation_id, "overview/evaluation-overview-analysis.html")


@check_evaluation_view_permission
def evaluation_findings_overview_view(request, evaluation_id):
    return evaluation_summary_view(request, evaluation_id, "overview/evaluation-overview-findings.html")


@check_evaluation_view_permission
def evaluation_cost_overview_view(request, evaluation_id):
    return evaluation_summary_view(request, evaluation_id, "overview/evaluation-overview-costs.html")


@login_required
def evaluation_summary_view(request, evaluation_id, page):
    evaluation = models.Evaluation.objects.get(pk=evaluation_id)
    user_can_edit = request.user in evaluation.users.all()
    interventions = models.Intervention.objects.filter(evaluation_id=evaluation.id)
    outcome_measures = models.OutcomeMeasure.objects.filter(evaluation_id=evaluation.id)
    other_measures = models.OtherMeasure.objects.filter(evaluation_id=evaluation.id)
    costs = models.EvaluationCost.objects.filter(evaluation_id=evaluation.id)
    processes_and_standards = models.ProcessStandard.objects.filter(evaluation_id=evaluation.id)
    evaluation_types = [
        evaluation_type[1]
        for evaluation_type in choices.EvaluationTypeOptions.choices
        if evaluation_type[0] in evaluation.evaluation_type
    ]
    topics = [topic[1] for topic in choices.Topic.choices if topic[0] in evaluation.topics]
    organisations = [
        organisation[1] for organisation in enums.Organisation.choices if organisation[0] in evaluation.organisations
    ]
    dates = models.EventDate.objects.filter(evaluation_id=evaluation.id)
    links = models.LinkOtherService.objects.filter(evaluation_id=evaluation.id)

    data = {
        "evaluation": evaluation,
        "user_can_edit": user_can_edit,
        "interventions": interventions,
        "outcome_measures": outcome_measures,
        "other_measures": other_measures,
        "costs": costs,
        "processes_and_standards": processes_and_standards,
        "date": dates,
        "links": [{"name": link.name_of_service, "link": link.link_or_identifier} for link in links],
        "evaluation_types": evaluation_types,
        "topics": topics,
        "organisations": organisations,
    }
    return render(request, page, {"data": data})
