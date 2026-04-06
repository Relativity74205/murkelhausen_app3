"""Lightweight heartbeat task for worker health monitoring."""

import logging

from django.tasks import task

from family_intranet.otel import METRIC_PREFIX, get_meter

logger = logging.getLogger(__name__)

HEARTBEAT_TASK_PATH = "family_intranet.jobs.heartbeat.worker_heartbeat"

_meter = get_meter("garmin")

_heartbeat_counter = _meter.create_counter(
    f"{METRIC_PREFIX}.worker.heartbeat",
    description="Heartbeat task executions",
)


@task
def worker_heartbeat() -> None:
    _heartbeat_counter.add(1)
    logger.debug("Worker heartbeat.")
