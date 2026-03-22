from django.core.management.base import BaseCommand

from family_intranet.jobs.garmin.runner import run_garmin_load


class Command(BaseCommand):
    help = "Enqueue the Garmin data load task"

    def handle(self, *_args: object, **_options: object) -> None:
        result = run_garmin_load.enqueue()
        self.stdout.write(f"Enqueued Garmin load task: {result.id}")
