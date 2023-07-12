from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from eva_reg.evaluation import (
    authentication_views,
    download_views,
    overview_views,
    submission_views,
    views,
)

initial_urlpatterns = [
    path("", submission_views.index_view, name="index"),
    path("search/", views.EvaluationSearchView, name="search"),
    path("my-evaluations/", views.my_evaluations_view, name="my-evaluations"),
    path("data-download/", download_views.download_page_view, name="data-download"),
    path(
        "evaluation/<uuid:evaluation_id>/overview/filter-users/",
        submission_views.filter_evaluation_overview_users_view,
        name="evaluation-overview-filter-users",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/overview/",
        submission_views.evaluation_overview_view,
        name="evaluation-overview",
    ),
]

account_urlpatterns = [
    path("accounts/verify/", authentication_views.CustomVerifyUserEmail, name="verify-email"),
    path("accounts/password-reset/", authentication_views.PasswordReset, name="password-reset"),
    path("accounts/change-password/reset/", authentication_views.PasswordChange, name="password-set"),
    path("accounts/login/", authentication_views.CustomLoginView, name="account_login"),
    path("accounts/signup/", authentication_views.CustomSignupView.as_view(), name="account_signup"),
    path("accounts/verify/resend/", authentication_views.CustomResendVerificationView, name="resend-verify-email"),
    path("accounts/accept-invite/", authentication_views.AcceptInviteSignupView, name="accept-invite"),
    path("accounts/", include("allauth.urls")),
]

evaluation_contributor_urlpatterns = [
    path(
        "evaluation-contributors/<uuid:evaluation_id>/",
        views.EvaluationContributor,
        name="evaluation-contributors",
    ),
    path(
        "evaluation-contributor-remove/<uuid:evaluation_id>/<str:email_to_remove>",
        views.evaluation_contributor_remove_view,
        name="evaluation-contributor-remove",
    ),
]

evaluation_entry_urlpatterns = [
    path("evaluation/create/", submission_views.create_evaluation, name="create-evaluation"),
    path("evaluation/<uuid:evaluation_id>/", submission_views.intro_page_view, name="intro"),
    path("evaluation/<uuid:evaluation_id>/title/", submission_views.evaluation_title_view, name="title"),
    path(
        "evaluation/<uuid:evaluation_id>/description/", submission_views.evaluation_description_view, name="description"
    ),
    path(
        "evaluation/<uuid:evaluation_id>/options/",
        submission_views.evaluation_options_view,
        name="options",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/issue-description/",
        submission_views.evaluation_issue_description_view,
        name="issue-description",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/studied-population/",
        submission_views.evaluation_studied_population_view,
        name="studied-population",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/participant-recruitment/",
        submission_views.evaluation_participant_recruitment,
        name="participant-recruitment",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/evaluation-types/",
        submission_views.evaluation_types_view,
        name="evaluation-types",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/impact-design/",
        submission_views.evaluation_impact_design_view,
        name="impact-design",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/impact-analysis/",
        submission_views.evaluation_impact_analysis_view,
        name="impact-analysis",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/process-design-aspects/",
        submission_views.evaluation_process_design_aspects_view,
        name="process-design-aspects",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/process-analysis/",
        submission_views.evaluation_process_analysis_view,
        name="process-analysis",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/economic-design/",
        submission_views.evaluation_economic_design_view,
        name="economic-design",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/economic-analysis/",
        submission_views.evaluation_economic_analysis_view,
        name="economic-analysis",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/other-design/",
        submission_views.evaluation_other_design_view,
        name="other-design",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/other-analysis/",
        submission_views.evaluation_other_analysis_view,
        name="other-analysis",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/ethics/",
        submission_views.evaluation_ethics_view,
        name="ethics",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/impact-findings/",
        submission_views.evaluation_impact_findings_view,
        name="impact-findings",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/economic-findings/",
        submission_views.evaluation_economic_findings_view,
        name="economic-findings",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/process-findings/",
        submission_views.evaluation_process_findings_view,
        name="process-findings",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/other-findings/",
        submission_views.evaluation_other_findings_view,
        name="other-findings",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/visibility/",
        submission_views.evaluation_visibility_view,
        name="visibility",
    ),
    path("evaluation/<uuid:evaluation_id>/end/", submission_views.end_page_view, name="end"),
    path(
        "evaluation/<uuid:evaluation_id>/overview/",
        submission_views.evaluation_overview_view,
        name="evaluation-overview",
    ),
]

intervention_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/interventions/",
        submission_views.summary_interventions_page_view,
        name="interventions",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/interventions/<uuid:intervention_id>/",
        submission_views.intervention_page_view,
        name="intervention-page",
    ),
]


outcome_measure_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/outcome-measures/",
        submission_views.summary_outcome_measure_page_view,
        name="outcome-measures",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/outcome-measures/<uuid:outcome_measure_id>/",
        submission_views.outcome_measure_page_view,
        name="outcome-measure-page",
    ),
]


other_measure_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/other-measures/",
        submission_views.summary_other_measure_page_view,
        name="other-measures",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/other-measures/<uuid:other_measure_id>/",
        submission_views.other_measure_page_view,
        name="other-measure-page",
    ),
]


processes_standards_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/processes-standards/",
        submission_views.summary_processes_standards_page_view,
        name="processes-standards",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/processes-standards/<uuid:process_standard_id>/",
        submission_views.process_standard_page_view,
        name="processes-standard-page",
    ),
]

grants_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/grants/",
        submission_views.summary_grants_page_view,
        name="grants",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/grants/<uuid:grant_id>/",
        submission_views.grant_page_view,
        name="grant-page",
    ),
]

evaluation_costs_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/evaluation-costs/",
        submission_views.summary_evaluation_costs_page_view,
        name="evaluation-costs",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/evaluation-costs/<uuid:evaluation_cost_id>/",
        submission_views.evaluation_cost_page_view,
        name="evaluation-cost-page",
    ),
]

documents_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/documents/",
        submission_views.summary_documents_page_view,
        name="documents",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/documents/<uuid:document_id>/",
        submission_views.document_page_view,
        name="document-page",
    ),
]

links_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/links/",
        submission_views.summary_links_page_view,
        name="links",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/links/<uuid:link_id>/",
        submission_views.links_page_view,
        name="link-page",
    ),
]


event_date_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/event-dates/",
        submission_views.summary_event_dates_page_view,
        name="event-dates",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/event-dates/<uuid:event_date_id>/",
        submission_views.event_date_page_view,
        name="event-date-page",
    ),
]

process_evaluation_methods_urlpatterns = [
    path(
        "evaluation/<uuid:evaluation_id>/process-evaluation-methods/",
        submission_views.summary_process_evaluation_methods_page_view,
        name="process-evaluation-methods",
    ),
    path(
        "evaluation/<uuid:evaluation_id>/process-evaluation-methods/<uuid:process_evaluation_method_id>/",
        submission_views.process_evaluation_method_page_view,
        name="process-evaluation-method-page",
    ),
]

evaluation_summary_urlpatterns = [
    path(
        "evaluation-summary/<uuid:evaluation_id>/",
        lambda request, evaluation_id: redirect("evaluation-summary-overview", evaluation_id=evaluation_id),
        name="evaluation-summary",
    ),
    path(
        "evaluation-summary/<uuid:evaluation_id>/overview/",
        overview_views.evaluation_summary_overview_view,
        name="evaluation-summary-overview",
    ),
    path(
        "evaluation-summary/<uuid:evaluation_id>/overview/measured/",
        overview_views.evaluation_measured_overview_view,
        name="evaluation-summary-measured",
    ),
    path(
        "evaluation-summary/<uuid:evaluation_id>/overview/design/",
        overview_views.evaluation_design_overview_view,
        name="evaluation-summary-design",
    ),
    path(
        "evaluation-summary/<uuid:evaluation_id>/overview/analysis/",
        overview_views.evaluation_analysis_overview_view,
        name="evaluation-summary-analysis",
    ),
    path(
        "evaluation-summary/<uuid:evaluation_id>/overview/findings/",
        overview_views.evaluation_findings_overview_view,
        name="evaluation-summary-findings",
    ),
    path(
        "evaluation-summary/<uuid:evaluation_id>/overview/cost/",
        overview_views.evaluation_cost_overview_view,
        name="evaluation-summary-cost",
    ),
]

feedback_and_help_urlpatterns = [path("feedback-and-help/", views.feedback_and_help_view, name="feedback-and-help")]

terms_and_conditions_urlpatterns = [
    path("terms-and-conditions/", views.terms_and_conditions_view, name="terms-and-conditions")
]

evaluation_edit_patterns = (
    evaluation_contributor_urlpatterns
    + evaluation_entry_urlpatterns
    + intervention_urlpatterns
    + outcome_measure_urlpatterns
    + other_measure_urlpatterns
    + grants_urlpatterns
    + processes_standards_urlpatterns
    + evaluation_costs_urlpatterns
    + documents_urlpatterns
    + links_urlpatterns
    + event_date_urlpatterns
    + process_evaluation_methods_urlpatterns
)

urlpatterns = (
    initial_urlpatterns
    + account_urlpatterns
    + evaluation_edit_patterns
    + evaluation_summary_urlpatterns
    + feedback_and_help_urlpatterns
    + terms_and_conditions_urlpatterns
)

debug_urlpatterns = [
    path("admin/", admin.site.urls),
    path("test/", views.beta_test_view, name="test"),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + debug_urlpatterns

handler404 = "eva_reg.evaluation.views.view_404"
