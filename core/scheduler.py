"""APScheduler background task scheduler."""

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from family_intranet.jobs.garmin.runner import run_garmin_load

_scheduler: BackgroundScheduler | None = None


def start() -> None:
    global _scheduler  # noqa: PLW0603
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler()
    _scheduler.add_jobstore(DjangoJobStore(), "default")
    _scheduler.remove_all_jobs()
    _scheduler.add_job(
        run_garmin_load,
        "cron",
        minute=0,
        id="garmin_load",
        replace_existing=True,
    )
    _scheduler.start()
