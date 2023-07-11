import json
import pathlib

import httpx

__here__ = pathlib.Path(__file__).parent
DATA_DIR = __here__ / ".." / "data"
APP_DIR = __here__ / ".." / "eva_reg" / "evaluation"

base_url = "https://www.gov.uk/api/organisations"

client = httpx.Client()


def get_results_and_next_url(url):
    response = client.get(url)
    data = response.json()
    links = {item["rel"]: item["href"] for item in data["_response_info"]["links"]}
    next_url = links.get("next", None)
    results = data.get("results", [])
    return results, next_url


def gather_results(start_url):
    next_url = start_url
    while next_url:
        results, next_url = get_results_and_next_url(next_url)
        for result in results:
            yield result


def dump_data(data):
    output_filename = DATA_DIR / "organisations_raw.json"
    with output_filename.open("w") as f:
        json.dump(data, f, indent=2)


def get_name(item):
    title = item["title"]
    abbreviation = item["details"]["abbreviation"]
    if abbreviation:
        title = f"{title} ({abbreviation})"
    return title


def dump_python(data):
    python_template = """
from . import utils

org_tuples = (
{org_tuples}
)
Organisation = utils.Choices("Organisation", org_tuples)
"""
    org_tuples = tuple((item["details"]["slug"], get_name(item)) for item in data)
    org_tuples = sorted(org_tuples, key=lambda x: x[1].lower())
    org_tuples = ",\n".join(repr(t) for t in org_tuples)
    content = python_template.format(org_tuples=org_tuples)
    output_filename = APP_DIR / "data.py"
    output_filename.write_text(content)


def main():
    results = list(gather_results(base_url))
    dump_data(results)
    dump_python(results)


if __name__ == "__main__":
    main()
