# Decision Log: APScheduler → Django Tasks Migration

## Decision 1: Replace APScheduler entirely (not keep as trigger)

**Options considered:**
- A) Keep APScheduler just for scheduling, have it call `task.enqueue()` instead of running directly
- B) Replace APScheduler entirely with system cron + Django tasks worker

**Chosen:** Option B

**Why:** The hybrid approach (A) introduces the worst of both worlds — you still carry APScheduler's in-process thread complexity, its DjangoJobStore, and its DB tables, while also adding django-tasks infrastructure. APScheduler's value is in-process scheduling; using it solely to call `.enqueue()` once per hour is massive overkill. System cron is a solved, zero-maintenance scheduling mechanism.

---

## Decision 2: Django 6.0 built-in tasks framework (not Celery, Django-Q2, Huey)

**Options considered:**
- Celery (requires Redis/RabbitMQ broker)
- Django-Q2 (Django-native, DB as broker)
- Huey (lightweight, Redis or SQLite)
- Django 6.0 `django.tasks` (official API, third-party backend)

**Chosen:** Django 6.0 `django.tasks`

**Why:** User preference. It's the official Django API going forward — aligns with the framework's direction. Avoids adding a heavy dependency like Celery for a single hourly job.

---

## Decision 3: Upgrade to Django 6.0 (not stay on 5.2)

**Context:** `django.tasks` was introduced experimentally in Django 5.2 and stabilized in 6.0.

**Chosen:** Upgrade to Django 6.0

**Why:** User preference for the stable version of the API rather than the experimental 5.2 backport.

---

## Decision 4: `django-tasks-db` as the backend (not RQ, not ImmediateBackend)

**Context:** Django 6.0 only ships ImmediateBackend (synchronous, no worker) and DummyBackend (testing). Production use requires a third-party backend. Available options:
- `django-tasks-db` — uses Django ORM / PostgreSQL as the queue
- `django-tasks-rq` — uses Redis via RQ

**Chosen:** `django-tasks-db`

**Why:** The project already uses PostgreSQL. Adding Redis would be unnecessary infrastructure for a personal intranet with a single hourly job. `django-tasks-db` is by the same author as the Django tasks framework prototype (Jake Howard / RealOrangeOne).

---

## Decision 5: Background worker in entrypoint (not separate Docker service)

**Options considered:**
- A) Single container: background `db_worker &` in `entrypoint.sh` before `runserver`
- B) Two containers: separate `murkel3-worker` service in `docker-compose.yml`

**Chosen:** Option A (single container)

**Why:** For a personal intranet with one job, a separate container is over-engineered. Backgrounding the worker in the entrypoint is simpler operationally. Can always split later if needed.

---

## Decision 6: Host cron for scheduling (not in-container cron)

**Chosen:** Host-level cron entry: `0 * * * * docker exec murkelhausen3 uv run python manage.py enqueue_garmin_load`

**Why:** Simplest approach — no cron daemon needed inside the container, no additional Docker service. The host already runs cron. The management command is idempotent (enqueues a task; if the worker is down, it queues up and runs when the worker restarts).

---

## Decision 7: Drop APScheduler tables via SQL (not migration stub)

**Options considered:**
- A) Manual SQL: `DROP TABLE` + `DELETE FROM django_migrations`
- B) Write a Django migration stub using `SeparateDatabaseAndState`

**Chosen:** Option A

**Why:** This is a personal project. The APScheduler tables contain only ephemeral job scheduling state with no downstream use. A migration stub adds complexity for no benefit here.