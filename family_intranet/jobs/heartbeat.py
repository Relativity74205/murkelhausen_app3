"""Lightweight heartbeat task for worker health monitoring."""

import logging

from django.tasks import task

logger = logging.getLogger(__name__)

HEARTBEAT_TASK_PATH = "family_intranet.jobs.heartbeat.worker_heartbeat"


@task
def worker_heartbeat() -> None:
    logger.debug("Worker heartbeat.")
