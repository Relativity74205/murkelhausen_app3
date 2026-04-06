# Murkelhausen App V3

## Background Tasks

Two-container architecture for scheduled and user-triggered background jobs.

**Components:**
- **APScheduler** (in Django server) — schedules jobs (hourly Garmin load, 2-min heartbeat) and enqueues them via `django.tasks`
- **django-tasks-db** (separate worker container) — executes enqueued tasks, stores results in PostgreSQL
- **Tasks page** (`/tasks/`) — shows scheduled jobs, recent task results, worker health, and manual "Jetzt starten" button

**Worker health monitoring:** APScheduler enqueues a lightweight heartbeat task every 2 minutes. The Django server checks the DB for recent successful heartbeats to determine if the worker is alive.

**Local development:**
```bash
# Terminal 1: Django server (includes APScheduler)
uv run python manage.py runserver

# Terminal 2: Task worker
uv run python manage.py db_worker

# Manual trigger:
uv run python manage.py enqueue_garmin_load
```

**Docker:** Two services in `docker-compose.yml` — `murkel3` (server) and `murkel3-worker` (worker), sharing the same PostgreSQL database.

## TODO

- [x] add an icon to the app
- [x] page load timeout for spinner
- [x] google calendar
    - [x] make the amount of days shown configurable, default is 7 days 
    - [x] closing new/update form shall reset the values
    - [x] after creating/updating an appointment, the form shall be closed immediately and after the google api confirmed the appointment, a success message shall be shown
- [x] work calendar
    - https://outlook.office365.com/owa/calendar/ab698696d55f495da6d8087de90e6bf8@auxmoney.com/224d53aba3a64df69329d8567eace684477164590746596125/S-1-8-1202830513-731510667-3198393615-1294255192/reachcalendar.ics 
- [ ] add tasks to google calendar
- [ ] add stundenpläne
- [ ] open-web-ui
- [ ] create main page with overview
- [ ] garmin health data
- [ ] create historization of weather data
- [ ] power data
- [ ] beowulf, pi-holes performance data