# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project: Murkelhausen App 3

Personal intranet website for the family. Django backend with server-side templates, HTMX for dynamic updates, and Bootstrap for styling.

## Stack
- **Backend**: Django 5.2, Python 3.13
- **Frontend**: Django templates + HTMX + Bootstrap 5.3
- **Database**: PostgreSQL (via psycopg3)
- **Package Manager**: uv

## Development Commands

```bash
uv run python manage.py runserver       # Start dev server
uv run python manage.py migrate         # Run migrations
uv run python manage.py createsuperuser # Create admin user
uv add <package>                        # Add dependency
```

### ⚠️ Code Quality — Run After Every Change
```bash
uv run ruff format .         # Format code
uv run ruff check . --fix    # Fix linting issues
uv run ty check .            # Type check (Astral ty)
```
All three must pass before changes are complete.

## Project Structure

```
family_intranet/          # Django project package
  settings.py             # All config (Google Calendar, Pi-hole, OWM, HTMX timeout)
  urls.py                 # Root URL config
  repositories/           # External API/scraping integrations (no Django deps)
    google_calendar.py    # Google Calendar API (service account auth)
    outlook_calendar.py   # Outlook ICS feed (read-only)
    fussballde.py         # fussball.de web scraping
    handballnordrhein.py  # hnr-handball.liga.nu web scraping
    mheg.py               # MHEG waste management API
    gymbroich.py          # Gymnasium Broich Vertretungsplan API
    pihole.py             # Pi-hole v6 API (session-based auth)
    pushover.py           # Pushover push notification API
    owm.py                # OpenWeatherMap API (one-call + current weather)
    owm_models.py         # Pydantic models for OWM responses
    owm_functions.py      # OWM data processing helpers
core/                     # Main Django app
  views.py                # All views
  urls.py                 # App URL config
  context_processors.py   # htmx_timeout → available in all templates
  templates/core/
    base.html             # Base template (HTMX config, timeout handler, favicon)
    home.html             # Landing page with Pi-hole control and Pushover button
    calendar.html / calendar_content.html
    work_calendar.html / work_calendar_content.html
    football_games.html / handball_games.html
    muelltermine.html / vertretungsplan.html / weather.html
```

## Architecture Patterns

**Views**: Each feature has a page view (`/feature/`) and a data view (`/feature/data/`) loaded via HTMX. The page view renders the shell; the data view does the actual work and returns a partial template.

**Repositories**: All external integrations live in `family_intranet/repositories/`. They use `requests` for HTTP, `cachetools.TTLCache` for caching, and Pydantic models for data. These have no Django dependencies.

**HTMX pattern**: Page loads a spinner → HTMX fires request to data endpoint → partial HTML replaces spinner. Timeout handler in `base.html` catches `htmx:timeout` and `htmx:sendError` events.

**Parallel loading**: The calendar view uses `ThreadPoolExecutor` to fetch multiple Google calendars concurrently.

**Scheduler**: `core/scheduler.py` runs a `BackgroundScheduler` with `DjangoJobStore` (persisted to PostgreSQL via `django-apscheduler`). Started in `core/apps.py::CoreConfig.ready()`, guarded to only run during `runserver` (not `migrate` or other management commands). Requires `django_apscheduler` in `INSTALLED_APPS` and a `migrate` run to create the `django_apscheduler_*` tables. Jobs visible in Django admin.

## Implemented Features & URLs

| Feature | URLs |
|---------|------|
| Home | `/` |
| Family Calendar (Google) | `/calendar/`, `/calendar/data/`, `/calendar/create/`, `/calendar/update/`, `/calendar/delete/` |
| Work Calendar (Outlook ICS) | `/work-calendar/`, `/work-calendar/data/` |
| Football (fussball.de scraping) | `/football/`, `/football/data/` |
| Handball (hnr-handball scraping) | `/handball/`, `/handball/data/` |
| Trash Collection (MHEG API) | `/muell/`, `/muell/data/` |
| Vertretungsplan (Gymbroich API) | `/vertretungsplan/`, `/vertretungsplan/data/` |
| Pi-hole control | `/pihole/status/`, `/pihole/disable/` |
| Weather (OpenWeatherMap) | `/weather/` |
| Pushover notifications | `/pushover/send/` |

## Configuration (Environment Variables)

```
# Google Calendar
GOOGLE_PRIVATE_KEY, GOOGLE_CLIENT_EMAIL
GOOGLE_CALENDAR_ARKADIUS, GOOGLE_CALENDAR_ERIK, GOOGLE_CALENDAR_MATTIS
GOOGLE_CALENDAR_ANDREA, GOOGLE_CALENDAR_GEBURTSTAGE

# Outlook
OUTLOOK_CALENDAR_URL

# Pi-hole
PIHOLE_PRIMARY_URL, PIHOLE_PRIMARY_PASSWORD
PIHOLE_BACKUP_URL, PIHOLE_BACKUP_PASSWORD  # optional

# OpenWeatherMap
OWM_API_KEY  # (check settings.py for exact name)

# Pushover
PUSHOVER_API_TOKEN, PUSHOVER_USER_KEY

# App
HTMX_TIMEOUT  # milliseconds, default 30000
```

## Code Quality Notes

- **Ruff** configured with strict Django rules; see `pyproject.toml` for per-file ignores
- **ty** type checker excludes: `mheg.py`, `pihole.py`, `owm*.py`, `google_calendar.py` (legacy code / missing stubs)
- `google_calendar.py` is excluded from ty due to external library type issues
- Formatting: double quotes, 88-char line length

## ⚠️ Auto-Documentation Policy

**Always update this CLAUDE.md when you:**
- Add new features, views, or URLs
- Add new repositories or dependencies
- Change project structure or architecture
