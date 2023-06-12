import csv
import pathlib

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand

DATA_DIR = settings.BASE_DIR / "temp-data"
CHUNK_SIZE = 16 * 1024


# Need maps for CSV headers to model property names


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
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
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
    with open(filename, 'r') as file:
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
    return rows


def import_and_upload_evaluations(url):
    filename = save_url_to_data_dir(url)
    headers = get_sheet_headers(filename)
    rows = get_data_rows(filename)
    unique_ids = get_evaluation_ids(rows, headers)
    for unique_id in unique_ids:
        rows_for_id = get_evaluation_rows_for_id(unique_id, rows, headers)
        transform_and_create_from_rows(rows_for_id)

