import csv
import pathlib

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand

DATA_DIR = settings.BASE_DIR / "temp-data"
CHUNK_SIZE = 16 * 1024


# Need maps for CSV headers to model property names

generic_headers = (
    "Evaluation title",  # evaluation title
    "Short title for evaluation",  # short title
    "Process",  # Process evaluation
    "Impact",  # Impact evaluation
    "Economic",  # Economic evaluation
    "Other evaluation type (please state)",  # Other evaluation
    "Government departments",  # Organisation
    "Evaluation summary",  # Description
    "Processes and standards",  # Processes and standards name
    "Issue to be addressed",  # Issue description
    "Who is expecting the issue",  # those experiencing the issue
    "Why the issue is important / why are improvements needed",  # why improvements matter
    "Who does it matter to",  # who improvements matter to
    "What difference the intervention intends to make",  # Issue relevance
    "Studied population including location(s)",  # Studied population
    "Eligibility criteria",  # Eligibility criteria
    "Total number of people (or other unit) included in the evaluation",  # Sample size
    "Type of unit",  # Sample size units
    "Referral / recruitment route",  # Process for recruitment
    "Referral / recruitment schedule",  # Recruitment schedule
    "Impact - Design",  # Impact evaluation design
    "Impact - Justification for design",  # Impact design justification
    "Impact - Features to reflect real-world implementation",  # Impact design features
    "Impact - Description",  # Impact design description
    "Impact - Equity",  # Impact design equity
    "Impact - Assumptions",  # Impact design assumptions
    "Impact - Limitations of approach",  # Impact design approach limitations
    "Economic - Costs included",  # Perspective: costs
    "Economic - Benefits included",  # Perspective: benefits
    "Economic - Monetisation approach",  # Economic evaluation montesiation approaches
    "Economic - Evaluation design",  # Economic evaluation design details,
    "Other - Evaluation design",  # Design type
    "Other - Summary of methods",  # Design details
    "Process - Description of analysis",  # Description of planned analysis
    "Impact - Analysis framework",  # Impact analysis Framework
    "Impact - Analysis basis",  # Analysis basis
    "Impact - Analysis set",  # Analysis set
    "Impact - Primary effect size measure type",  # Primary effect size measure type
    "Impact - Primary effect size measure",  # Primary effect size measure
    "Impact - Primary effect size measure interval",  # Primary effect size measure interval
    "Impact - Primary effect size measure description",  # Primary effect size measure description
    "Impact - Interpretation type",  # Interpretation type
    "Impact - Sensitivity analysis",  # Sensitivity analysis
    "Impact - Subgroup analysis",  # Subgroup analysis
    "Impact - Missing data handling",  # Missing data handling
    "Impact - Fidelity of report",  # Fidelity reporting
    "Impact - Description of analysis",  # Description of planned analysis
    "Economic - Description of analysis",  # Description of planned analysis
    "Other - Description of analysis",  # Description of planned analysis
    "Process - Summary of findings",  # Summary findings
    "Process - Findings",  # Findings
    "Economic - Summary of findings",  # Summary findings
    "Economic - Findings",  # Findings
    "Other - Summary of findings",  # Summary findings
    "Other - Findings",  # Findings
    "Ethics committee approval",  # Ethics committee approval
    "Ethics committee details",  # Ethics committee details
    "Ethical state of study given existing evidence base",  # Ethical state of study given existing evidence base
    "Risks to participants",  # Risks to participants
    "Risks to study team",  # Risks to study team
    "Participant involvement",  # Participant involvement
    "Participant consent (if no, why not)",  # Participant consent
    "Participant information",  # Participant information
    "Participant payment (if yes, please elaborate)",  # Participant payment
    "Confidentiality and personal data",  # Confidentiality and personal data
    "Breaking confidentiality",  # Breaking confidentiality
    "Other ethical information",  # Other ethical information
)

# Outcome measure
outcome_measure_headers = (
    "Outcome title",  # Outcome name
    "Primary or secondary outcome",  # Primary or secondary
    "Direct or surrogate",  # Direct or surrogate
    "Measure type",  # Measure type
    "Description of measure",  # Description of measure
    "Collection procedures",  # Collection process
    "Time point of interest (Month)",  # Timepoint(s) of interest
    "Time point of interest (Year)",  # Timepoint(s) of interest
    "Minimum practically important difference",  # Minimum practically important difference
    "Relevance of outcome",  # Relevance of outcome
)

# Other measure
other_measure_headers = (
    "Other outcomes - Outcome name",  # Measurement name
    "Other outcomes - Outcome measure type",  # Measure type
    "Other outcomes - Description of measure",  # Description of measurement
    "Other outcomes - Collection procedures and timing",  # Collection procedures and timing
)

# Grants
grant_headers = ()

# Links
links_headers = ("Links to associated docments",)  # intentional typo in csv file. Links

# Interventions
intervention_headers = (
    "Intervention name",  # Intervention name
    "Intervention brief description",  # Intervention brief description
    "Intervention rationale",  # Intervention rationale
    "Materials used",  # Intervention materials used
    "Procedures used",  # Intervention procedures
    "Who delivered the intervention",  # Intervention provider description
    "How was the intervention delivered",  # Intervention modes of delivery
    "Where was the intervention delivered",  # Intervention location
    "How often the intervention was delivered",  # Intervention frequency of delivery
    "Tailoring",  # Intervention tailoring
    "How well it was delivered (fidelity)",  # Intervention fidelity
    "Resource requirements",  # Intervention resource requirements
    "Geographical information",  # Intervention geographical information
    "Intervention start date (Month)",  # Intervention - when ?
    "Intervention start date (Year)",  # Intervention - when ?
    "Intervention end date (Month)",  # Intervention - when ?
    "Intervention end date (Year)",  # Intervention - when ?
)

# Event dates
event_date_headers = ()

# Evaluation costs
evaluation_cost_headers = ("Evaluation cost (£)",)  # Not sure

# Processes and standards
processes_and_standards_headers = (
    "Name of standard or process",  # Name of standard of process
    "Conformity",  # Conformity of standard or process
    "Process and standards - Description",  # Description of standard or process
)

all_headers = (
    generic_headers
    + outcome_measure_headers
    + other_measure_headers
    + grant_headers
    + links_headers
    + intervention_headers
    + event_date_headers
    + evaluation_cost_headers
    + processes_and_standards_headers
)


class Command(BaseCommand):
    help = "Populate Evaluation Registry with data from RSM"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--url", type=str, help="URL of data to upload")

    def handle(self, *args, **kwargs):
        url = kwargs["url"]
        import_and_upload_evaluations(url)


def save_url_to_data_dir(url):
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
    with open(filename, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
    for header in headers:
        print(header)
    return headers


def get_evaluation_ids(data, headers):
    unique_ids = set()
    column_index = headers.index("Evaluation ID")
    for row in data:
        id_value = row[column_index]
        if id_value:
            unique_ids.add(id_value)
    return sorted(unique_ids)


def get_data_rows(filename):
    data = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        _ = next(reader)
        for row in reader:
            data.append(row)
        return data


def get_evaluation_rows_for_id(unique_id, rows, headers):
    column_index = headers.index("Evaluation ID")
    matching_rows = [row for row in rows if row[column_index] == unique_id]
    return matching_rows


def transform_and_create_from_rows(rows):
    # print(rows)
    return rows


def import_and_upload_evaluations(url):
    filename = save_url_to_data_dir(url)
    headers = get_sheet_headers(filename)
    rows = get_data_rows(filename)
    unique_ids = get_evaluation_ids(rows, headers)
    unique_id = unique_ids[0]
    rows_for_id = get_evaluation_rows_for_id(unique_id, rows, headers)
    transform_and_create_from_rows([rows_for_id[0]])
    # for unique_id in unique_ids:
    #     rows_for_id = get_evaluation_rows_for_id(unique_id, rows, headers)
    #     transform_and_create_from_rows(rows_for_id)
