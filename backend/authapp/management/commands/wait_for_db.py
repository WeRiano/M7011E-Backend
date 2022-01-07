import time

from psycopg2 import OperationalError as Psycopg20pError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database ...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg20pError, OperationalError):
                wait_seconds = 1
                self.stdout.write("Database unavailable, waiting " + str(wait_seconds) + " second")
                time.sleep(wait_seconds)

            self.stdout.write(self.style.SUCCESS("Database ready!"))