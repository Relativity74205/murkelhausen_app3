import os
import sys

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        # Only start the scheduler when actually serving requests.
        # Skip for management commands (migrate, shell, etc.) and the autoreload
        # parent process (runserver calls ready() twice; only run in child).
        _management_commands = {
            "migrate",
            "makemigrations",
            "shell",
            "test",
            "collectstatic",
        }
        if set(sys.argv) & _management_commands:
            return
        if "runserver" in sys.argv and os.environ.get("RUN_MAIN") != "true":
            return
        from core import scheduler  # noqa: PLC0415

        scheduler.start()
