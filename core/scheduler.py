"""APScheduler background task scheduler."""

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from family_intranet.jobs.garmin.runner import run_garmin_load
from family_intranet.jobs.heartbeat import worker_heartbeat

_scheduler: BackgroundScheduler | None = None


def _enqueue_garmin_load() -> None:
    run_garmin_load.enqueue()


def _enqueue_heartbeat() -> None:
    worker_heartbeat.enqueue()


def start() -> None:
    global _scheduler  # noqa: PLW0603
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler()
    _scheduler.add_jobstore(DjangoJobStore(), "default")
    _scheduler.remove_all_jobs()
    _scheduler.add_job(
        _enqueue_garmin_load,
        "cron",
        minute=0,
        id="garmin_load",
        replace_existing=True,
    )
    _scheduler.add_job(
        _enqueue_heartbeat,
        "interval",
        minutes=2,
        id="worker_heartbeat",
        replace_existing=True,
    )
    _scheduler.start()
