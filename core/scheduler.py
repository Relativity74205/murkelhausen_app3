"""APScheduler background task scheduler."""

import random
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

RANDOM_NUMBER_FILE = Path(__file__).parent / "random_number.txt"

_scheduler: BackgroundScheduler | None = None


def _write_random_number() -> None:
    number = random.randint(1, 1_000_000)
    RANDOM_NUMBER_FILE.write_text(str(number))


def start() -> None:
    global _scheduler  # noqa: PLW0603
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler()
    _scheduler.add_jobstore(DjangoJobStore(), "default")
    _scheduler.add_job(
        _write_random_number,
        "interval",
        seconds=10,
        id="random_number",
        replace_existing=True,
    )
    _write_random_number()  # write immediately on startup
    _scheduler.start()
