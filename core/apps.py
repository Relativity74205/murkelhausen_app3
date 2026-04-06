import os
import sys

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        # Skip all management commands (migrate, shell, etc.) — only run when serving.
        # For runserver, also skip the autoreload parent (ready() is called twice).
        is_manage_py = bool(sys.argv) and sys.argv[0].endswith("manage.py")
        is_runserver = "runserver" in sys.argv
        is_db_worker = "db_worker" in sys.argv

        if is_manage_py and not is_runserver and not is_db_worker:
            return
        if is_runserver and os.environ.get("RUN_MAIN") != "true":
            return

        from family_intranet.otel import setup_otel  # noqa: PLC0415

        setup_otel(instrument_django=not is_db_worker)

        if not is_db_worker:
            from core import scheduler  # noqa: PLC0415

            scheduler.start()
