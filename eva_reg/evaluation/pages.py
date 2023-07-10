import itertools

from etf.evaluation import choices, utils


class EvaluationPageStatus(utils.Choices):
    DONE = "Completed"
    IN_PROGRESS = "In progress"
    INCOMPLETE = "Incomplete"
    NOT_STARTED = "Not started"


page_display_names = {
    "intro": "Intro",
    "title": "Title",
    "options": "Optional information",
    "description": "Description and organisations",
    "issue-description": "Issue description",
    "studied-population": "Studied population",
    "participant-recruitment": "Participant recruitment",
    "evaluation-costs": "Evaluation costs",
    "event-dates": "Event dates",
    "evaluation-types": "Evaluation types",
    "impact-design": "Impact evaluation design",
    "impact-analysis": "Impact evaluation analysis",
    "process-design-aspects": "Process evaluation design: Aspects to investigate",
    "process-evaluation-methods": "Process evaluation design methods",
    "process-analysis": "Process evaluation analysis",
    "economic-design": "Economic evaluation design",
    "economic-analysis": "Economic evaluation analysis",
    "other-design": "Other evaluation design",
    "other-analysis": "Other evaluation analysis",
    "interventions": "Interventions",
    "outcome-measures": "Outcome measures",
    "other-measures": "Other measures",
    "ethics": "Ethical considerations",
    "impact-findings": "Impact evaluation findings",
    "economic-findings": "Economic evaluation findings",
    "process-findings": "Process evaluation findings",
    "other-findings": "Other evaluation findings",
    "processes-standards": "Processes and standards",
    "grants": "Grants",
    "links": "Links and IDs",
    "visibility": "Evaluation visibility",
    "end": "End",
}

section_display_names = {
    "general": "General",
    "interventions-and-measures": "Interventions and measures",
    "design-analysis": "Design and analysis",
    "findings": "Findings",
    "further-information": "Further information",
}

section_pages = {
    "general": (
        "intro",
        "title",
        "options",
        "description",
        "event-dates",
        "evaluation-types",
        "issue-description",
    ),
    "interventions-and-measures": (
        "interventions",
        "outcome-measures",
        "other-measures",
    ),
    "design-analysis": (
        "studied-population",
        "participant-recruitment",
        "impact-design",
        "impact-analysis",
        "economic-design",
        "economic-analysis",
        "process-design-aspects",
        "process-evaluation-methods",
        "process-analysis",
        "other-design",
        "other-analysis",
    ),
    "findings": (
        "impact-findings",
        "economic-findings",
        "process-findings",
        "other-findings",
    ),
    "further-information": (
        "processes-standards",
        "evaluation-costs",
        "grants",
        "links",
        "ethics",
    ),
}

page_url_names = (
    "intro",
    "title",
    "options",
    "description",
    "issue-description",
    "studied-population",
    "participant-recruitment",
    "evaluation-costs",
    "evaluation-types",
    "event-dates",
    "impact-design",
    "impact-analysis",
    "process-design-aspects",
    "process-evaluation-methods",
    "process-analysis",
    "economic-design",
    "economic-analysis",
    "other-design",
    "other-analysis",
    "interventions",
    "outcome-measures",
    "other-measures",
    "ethics",
    "impact-findings",
    "economic-findings",
    "process-findings",
    "other-findings",
    "processes-standards",
    "grants",
    "links",
    "visibility",
    "end",
)

object_page_url_names = {
    "interventions": "intervention-page",
    "outcome-measures": "outcome-measure-page",
    "other-measures": "other-measure-page",
    "processes-standards": "processes-standard-page",
    "grants": "grant-page",
    "evaluation-costs": "evaluation-cost-page",
    "links": "link-page",
    "event-dates": "event-date-page",
    "process-evaluation-methods": "process-evaluation-method-page",
}

evaluation_type_page_mapping = {
    "IMPACT": set(("impact-analysis", "impact-design", "impact-findings")),
    "PROCESS": set(("process-analysis", "process-design-aspects", "process-evaluation-methods", "process-findings")),
    "ECONOMIC": set(("economic-analysis", "economic-design", "economic-findings")),
    "OTHER": set(("other-analysis", "other-design", "other-findings")),
}

page_options_mapping = {
    "issue_description_option": "issue-description",
    "ethics_option": "ethics",
    "grants_option": "grants",
}

all_evaluation_type_pages = set().union(*evaluation_type_page_mapping.values())
all_other_optional_pages = set(page_options_mapping.values())


def get_prev_next_page_name(page_name, page_options):
    pages = tuple(get_page_name_and_order(page_options).keys())
    assert page_name in pages
    page_index = pages.index(page_name)
    if page_index == 0:
        prev_url_name = None
    else:
        prev_url_name = pages[page_index - 1]
    if page_index + 1 == len(pages):
        next_url_name = None
    else:
        next_url_name = pages[page_index + 1]
    return prev_url_name, next_url_name


default_page_statuses = {page_name: EvaluationPageStatus.NOT_STARTED.name for page_name in page_url_names}


@utils.dictify
def get_page_name_and_order(page_options):
    evaluation_types = page_options["evaluation_types"]
    evaluation_pages_to_keep = set().union(
        *(evaluation_type_page_mapping.get(evaluation_type, set()) for evaluation_type in evaluation_types)
    )
    optional_pages_to_keep = set()
    for k, v in page_options.items():
        if k in page_options_mapping.keys() and v == choices.YesNo.YES.value:
            optional_pages_to_keep.add(page_options_mapping[k])

    evaluation_pages_to_remove = all_evaluation_type_pages - evaluation_pages_to_keep
    other_optional_pages_to_remove = all_other_optional_pages - optional_pages_to_keep
    pages_to_remove = evaluation_pages_to_remove.union(other_optional_pages_to_remove)
    counter = itertools.count(0)

    for page_name in page_url_names:
        if page_name not in pages_to_remove:
            yield page_name, next(counter)


def get_default_page_statuses():
    return dict(default_page_statuses)


def get_section_title(section):
    return section_display_names[section] or section
