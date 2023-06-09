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
        header = next(reader)
    return header

def get_evaluation_ids():

def get_evaluation_rows_for_id():

def transform_and_create_from_row():

def import_and_upload_evaluations(url):
    filename = save_url_to_data_dir(url)
    headers = get_sheet_headers(filename)
    print(headers)

