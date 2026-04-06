# Plan: Migrate from APScheduler to Django Tasks + django-tasks-db

## Context

The Garmin data loader currently runs as an APScheduler background job inside the Django process. This causes issues (stale jobs in DB, connection problems in background threads, tight coupling). The goal is to decouple scheduling from task execution using Django 6.0's built-in tasks framework with the `django-tasks-db` database backend.

**Architecture change:** APScheduler (in-process thread) → Django tasks (separate worker process) + system cron (scheduling).

## Files to Change

| File | Action |
|------|--------|
| `pyproject.toml` | Modify deps |
| `family_intranet/settings.py` | Replace `django_apscheduler` → `django_tasks_db`, add `TASKS` |
| `core/apps.py` | Remove scheduler startup from `ready()` |
| `core/scheduler.py` | Delete |
| `family_intranet/jobs/garmin/runner.py` | Add `@task` decorator |
| `core/management/__init__.py` | New (empty) |
| `core/management/commands/__init__.py` | New (empty) |
| `core/management/commands/enqueue_garmin_load.py` | New — management command |
| `entrypoint.sh` | Add db_worker process |
| `docker-compose.yml` | Add Garmin env vars, add worker service |
| `CLAUDE.md` | Update docs |

## Steps

### 1. Upgrade dependencies (`pyproject.toml`)
- `django>=5.2.6,<6.0` → `django>=6.0,<7.0`
- Remove `apscheduler>=3.10,<4.0` and `django-apscheduler>=0.7.0`
- Add `django-tasks-db>=0.12.0`
- Run `uv sync`

### 2. Update settings (`family_intranet/settings.py`)
- Replace `"django_apscheduler"` with `"django_tasks_db"` in `INSTALLED_APPS`
- Add:
```python
TASKS = {
    "default": {
        "BACKEND": "django_tasks_db.DatabaseBackend",
        "QUEUES": ["default"],
    }
}
```

### 3. Run migrations
```bash
uv run python manage.py migrate
```

### 4. Clean up old APScheduler tables (SQL)
```sql
DROP TABLE IF EXISTS django_apscheduler_djangojobexecution;
DROP TABLE IF EXISTS django_apscheduler_djangojob;
DELETE FROM django_migrations WHERE app = 'django_apscheduler';
```

### 5. Add `@task` decorator to runner (`family_intranet/jobs/garmin/runner.py`)
```python
from django.tasks import task

@task
def run_garmin_load():
    ...  # existing body unchanged
```

### 6. Delete `core/scheduler.py`

### 7. Simplify `core/apps.py`
Remove the entire `ready()` method and its imports — just keep `CoreConfig` with `name = "core"`.

### 8. Create management command
New file `core/management/commands/enqueue_garmin_load.py`:
```python
from django.core.management.base import BaseCommand
from family_intranet.jobs.garmin.runner import run_garmin_load

class Command(BaseCommand):
    help = "Enqueue the Garmin data load task"

    def handle(self, *args, **options):
        result = run_garmin_load.enqueue()
        self.stdout.write(f"Enqueued Garmin load task: {result.id}")
```

### 9. Update `entrypoint.sh`
```bash
#!/usr/bin/env bash
set -e
uv run python manage.py migrate
uv run python manage.py db_worker --no-reload &
uv run python manage.py runserver 0.0.0.0:8000
```

### 10. Update `docker-compose.yml`
- Add Garmin env vars (`GARMIN_EMAIL`, `GARMIN_PASSWORD`, `GARMIN_DB_*`)
- Add cron scheduling (host cron: `0 * * * * docker exec murkelhausen3 uv run python manage.py enqueue_garmin_load`)

### 11. Code quality + CLAUDE.md update

## Dev Workflow (after migration)

```bash
# Terminal 1: Django server
uv run python manage.py runserver

# Terminal 2: Task worker (auto-reloads in DEBUG)
uv run python manage.py db_worker

# Trigger Garmin load manually:
uv run python manage.py enqueue_garmin_load
```

## Verification
1. `uv run python manage.py check` — no Django 6.0 issues
2. `uv run python manage.py migrate` — creates django_tasks_db tables
3. Start `db_worker` in one terminal, `runserver` in another
4. Run `uv run python manage.py enqueue_garmin_load` — verify task appears in worker output
5. Check Django admin for task results
6. `uv run ruff format . && uv run ruff check . --fix && uv run ty check .` — all pass
