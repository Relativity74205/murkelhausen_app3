import logging
import os
import sys

from django.apps import AppConfig

logger = logging.getLogger(__name__)


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

        if is_db_worker:
            from django.utils import timezone  # noqa: PLC0415
            from django_tasks_db.models import DBTaskResult  # noqa: PLC0415

            count = DBTaskResult.objects.filter(status="RUNNING").update(
                status="FAILED",
                finished_at=timezone.now(),
                exception_class_path="",
                traceback="Abgebrochen: Worker-Prozess wurde beendet",
            )
            if count:
                logger.warning(
                    "Marked %d abandoned task(s) as FAILED on worker startup", count
                )
        else:
            from core import scheduler  # noqa: PLC0415

            scheduler.start()
