import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Waiting for the database to become available"

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database connection...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("Database not ready yet, retry in 1 second...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database connection established!"))
