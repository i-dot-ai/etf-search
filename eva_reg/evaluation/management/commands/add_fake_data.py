from django.core.management.base import BaseCommand

from eva_reg.evaluation import fakers


class Command(BaseCommand):
    help = "Add some fake data to populate database"

    def add_arguments(self, parser):
        parser.add_argument("-n", "--number", type=int, default=128, help="How many users to add")

    def handle(self, *args, **kwargs):
        number = kwargs["number"]

        for user in fakers.add_users(number):
            print(f"Added: {user}")  # noqa: T201
