"""Worker health check via heartbeat tasks in the shared database."""

from datetime import timedelta

from django.utils import timezone

from family_intranet.jobs.heartbeat import HEARTBEAT_TASK_PATH


def get_status() -> dict:  # type: ignore[type-arg]
    """Check worker health by looking for recent successful heartbeat tasks."""
    from django_tasks_db.models import DBTaskResult  # noqa: PLC0415

    cutoff = timezone.now() - timedelta(minutes=5)

    last_heartbeat = (
        DBTaskResult.objects.filter(task_path=HEARTBEAT_TASK_PATH, status="SUCCESSFUL")
        .order_by("-finished_at")
        .first()
    )

    if (
        last_heartbeat
        and last_heartbeat.finished_at
        and last_heartbeat.finished_at >= cutoff
    ):
        return {"state": "healthy", "last_seen": last_heartbeat.finished_at}

    if last_heartbeat:
        return {"state": "unhealthy", "last_seen": last_heartbeat.finished_at}

    return {"state": "unknown"}
