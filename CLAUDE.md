# Project: Murkelhausen App 3

## ⚠️ CRITICAL INSTRUCTIONS FOR CLAUDE CODE

### Auto-Documentation Policy
**ALWAYS update this CLAUDE.md file whenever you:**
1. Add a new feature or functionality
2. Create new views, URLs, or templates
3. Modify project structure or architecture
4. Add new dependencies or tools
5. Change development workflows

**When documenting features:**
- Add implementation details to "Implemented Features" section
- Update file locations in "Key Files & Locations"
- Move completed items from "Next Steps" to "Implemented Features"
- Document any new URLs, views, or templates created
- Note any new dependencies added

## Project Overview
- **Purpose**: Personal intranet website for the family
- New project starting from scratch
- Working directory: /Users/arkadius/dev/murkelhausen_app3
- Not currently a git repository

## Features & Requirements
- Family calendar (Google Calendar backend integration)
- Kids' football/handball games (scraped from external websites)
- Additional information display (from APIs and web scraping)
- Database storage for custom data

## Technology Decisions

### Final Stack
- **Backend**: Django (Python 3.13)
- **Frontend**: Django server-side templates + HTMX + Bootstrap CSS
- **Database**: PostgreSQL (to be implemented later)
- **Package Manager**: uv (Python project manager)

### Decision Rationale
- **Django**:
  - Built-in admin panel for family data management
  - Robust authentication system
  - Easy integration with existing Python scraping code
  - Template system works well with server-side rendering
- **HTMX**:
  - Simple, minimal JavaScript for dynamic interactions
  - Perfect for family intranet complexity level
  - Works seamlessly with Django templates
- **Bootstrap**:
  - Component-based approach matches Django philosophy
  - No build step complexity (CDN-ready)
  - Pre-built components speed up development
  - HTMX-friendly for partial page updates
- **uv**:
  - Modern, fast Python package manager
  - Better dependency resolution than pip
- **Python 3.13**:
  - Latest stable version with performance improvements
- **PostgreSQL**:
  - Robust database for family data storage
  - Good Django integration

## Important Facts

### Project Structure
- **Project Name**: `family_intranet` (Django project)
- **Main App**: `core` (handles home page and main functionality)
- **Python Version**: 3.13.5 (managed by uv)
- **Django Version**: 5.2.6
- **Virtual Environment**: `.venv` (created by uv)

### Key Files & Locations
- **Settings**: `family_intranet/settings.py` (configured with django-htmx)
- **Main URLs**: `family_intranet/urls.py` (includes core.urls)
- **Core URLs**: `core/urls.py` (home, calendar, calendar_data, calendar_create, calendar_delete, football_games, handball_games, muelltermine, vertretungsplan, pihole_status, pihole_disable)
- **Core Views**: `core/views.py` (home, calendar, calendar_data, calendar_create, calendar_delete, football_games, handball_games, muelltermine, vertretungsplan, pihole_status, pihole_disable)
- **Templates**:
  - `core/templates/core/home.html` (Bootstrap + HTMX)
  - `core/templates/core/calendar.html` (Family calendar display)
  - `core/templates/core/football_games.html` (Football schedule display)
  - `core/templates/core/handball_games.html` (Handball schedule display)
  - `core/templates/core/muelltermine.html` (Trash collection schedule)
  - `core/templates/core/vertretungsplan.html` (School substitution schedule)
- **Repositories**:
  - `family_intranet/repositories/google_calendar.py` (Google Calendar API integration)
  - `family_intranet/repositories/fussballde.py` (Football web scraping)
  - `family_intranet/repositories/handballnordrhein.py` (Handball web scraping)
  - `family_intranet/repositories/mheg.py` (MHEG waste management API)
  - `family_intranet/repositories/gymbroich.py` (Gymnasium Broich Vertretungsplan API)
  - `family_intranet/repositories/pihole.py` (Pi-hole DNS blocking control API)
- **Dependencies**: `pyproject.toml` (managed by uv)

### Implemented Features

#### 1. Home Page
- **Status**: ✅ Complete
- **Location**: `core/templates/core/home.html`
- **Description**: Fully functional landing page with Bootstrap 5.3 styling
- **Features**:
  - Responsive navbar with navigation links
  - Hero section with gradient background
  - Feature cards showcasing available functionality
  - HTMX loading indicators
  - Custom CSS for styling

#### 2. Family Calendar
- **Status**: ✅ Complete
- **URLs**:
  - `/calendar/` (view appointments)
  - `/calendar/data/` (HTMX data endpoint)
  - `/calendar/create/` (POST endpoint to create appointments)
  - `/calendar/delete/` (POST endpoint to delete appointments)
- **Views**:
  - `core.views.calendar` (`core/views.py:209-211`)
  - `core.views.calendar_data` (`core/views.py:214-249`)
  - `core.views.calendar_create` (`core/views.py:252-347`)
  - `core.views.calendar_delete` (`core/views.py:350-401`)
- **Template**: `core/templates/core/calendar.html`, `core/templates/core/calendar_content.html`
- **Repository**: `family_intranet/repositories/google_calendar.py`
- **Description**: Displays all family calendar appointments for the next 7 days from Google Calendar, with ability to create and delete appointments
- **Features**:
  - Fetches appointments from all configured family calendars (Arkadius, Familie, Erik, Mattis, Andrea, Geburtstage)
  - Displays appointments grouped by date
  - Shows appointment time (or "Ganztägig" for all-day events)
  - Color-coded calendar badges for each family member:
    - Arkadius (blue)
    - Erik (green)
    - Mattis (yellow)
    - Andrea (pink)
    - Geburtstage (red)
  - Recurring event badge for repeating appointments
  - Multi-day event support with date range display
  - **Create New Appointments**:
    - Modal form with calendar selection dropdown
    - Fields: event name, start/end date/time, description
    - Whole-day event checkbox (disables time fields)
    - Auto-fills end date to match start date
    - HTMX form submission with success/error messages
    - Automatically reloads calendar after successful creation
    - Form validation and error handling
  - **Delete Appointments**:
    - Delete button on each appointment card
    - Confirmation dialog before deletion
    - Visual feedback during deletion (button shows "⏳ Löschen...")
    - Success indicator (button shows "✅ Gelöscht")
    - Automatically reloads calendar after successful deletion
    - Error handling for network/API issues
  - HTMX async loading with spinner
  - Error handling for network/API issues
  - Responsive Bootstrap layout with card-based design
- **Dependencies**: gcsa, google-api-python-client, pydantic, babel, pytz, python-dateutil
- **Data Model**: `Appointment` Pydantic BaseModel with fields:
  - id, calendar_id, calendar_name (str | None)
  - event_name (str)
  - start_timestamp, end_timestamp (datetime)
  - start_date, end_date (date)
  - start_time, end_time (str)
  - days_string (str) - formatted date range
  - is_whole_day, is_recurring (bool)
- **API**: Google Calendar API via service account authentication
- **Configuration**:
  - Service account credentials in environment variables:
    - `GOOGLE_PRIVATE_KEY`
    - `GOOGLE_CLIENT_EMAIL`
  - Calendar IDs for each family member:
    - `GOOGLE_CALENDAR_ARKADIUS`
    - `GOOGLE_CALENDAR_ERIK`
    - `GOOGLE_CALENDAR_MATTIS`
    - `GOOGLE_CALENDAR_ANDREA`
    - `GOOGLE_CALENDAR_GEBURTSTAGE`
  - Configured in `family_intranet/settings.py` as `GOOGLE_CALENDAR_SETTINGS`
- **Code Quality Notes**:
  - google_calendar.py excluded from type checking (ty) due to external library type issues
  - Per-file ruff ignores for legacy code patterns: SIM102, RET504, TRY003, EM102, DTZ011, B905, PLW2901, PLW0127, C416

#### 3. Football Games Schedule
- **Status**: ✅ Complete
- **URL**: `/football/`
- **View**: `core.views.football_games` (`core/views.py:44-56`)
- **Template**: `core/templates/core/football_games.html`
- **Repository**: `family_intranet/repositories/fussballde.py`
- **Description**: Web scraping feature for VfB Speldorf football teams
- **Features**:
  - Scrapes game schedules from https://www.fussball.de
  - Tab-based interface with two teams: E2-Junioren and VfB Speldorf (Heimspiele)
  - Shows game date, time, game type, teams, and results
  - Error handling for network issues
  - Responsive Bootstrap layout with card-based design
  - E2-Junioren as default tab
- **Dependencies**: requests, beautifulsoup4
- **Data Model**: Dictionary with fields:
  - game_date (date)
  - time (str)
  - game_type (str)
  - home_team, away_team (str)
  - result (str | None)

#### 4. Handball Games Schedule
- **Status**: ✅ Complete
- **URL**: `/handball/`
- **View**: `core.views.handball_games` (`core/views.py:21-41`)
- **Template**: `core/templates/core/handball_games.html`
- **Repository**: `family_intranet/repositories/handballnordrhein.py`
- **Description**: Web scraping feature for DJK Saarn handball teams
- **Features**:
  - Scrapes game schedules from https://hnr-handball.liga.nu
  - Tab-based interface with two teams: D-Jugend and Erste Herren
  - Shows game date, time, location, teams, and results
  - Links to official game reports (Spielbericht) and group standings (Tabelle)
  - Badges for special cases: "Spielfrei" (free date), "Verlegt" (postponed)
  - Error handling for network issues
  - Responsive Bootstrap layout with card-based design
  - D-Jugend as default tab
- **Dependencies**: requests, beautifulsoup4, babel
- **Data Model**: `HandballGame` dataclass with fields:
  - game_date (date | None)
  - game_date_formatted (str)
  - time (str | None)
  - time_original (str | None) - for postponed games
  - home_team, away_team, location (str)
  - result (str | None)
  - link_to_spielbericht (str | None)
  - spielbericht_genehmigt (bool | None)
  - spielfrei (bool | None)

#### 5. Mülltermine (Trash Collection Schedule)
- **Status**: ✅ Complete
- **URL**: `/muell/`
- **View**: `core.views.muelltermine` (`core/views.py:73-81`)
- **Template**: `core/templates/core/muelltermine.html`
- **Repository**: `family_intranet/repositories/mheg.py`
- **Description**: Displays upcoming trash collection dates from MHEG waste management API
- **Features**:
  - Fetches collection schedule for configured address
  - Color-coded badges for different waste types:
    - Restmüll (gray)
    - Papier (blue)
    - Gelbe Tonne (yellow)
    - Biotonne (green)
    - Weihnachtsbaum (red)
  - Special badges for "Heute" (today) and "Morgen" (tomorrow)
  - Shows days until collection
  - Error handling for API/network issues
  - Responsive Bootstrap layout with card-based design
- **Dependencies**: requests, babel, pydantic, cachetools, python-dateutil
- **Data Model**: `MuellTermine` Pydantic BaseModel with fields:
  - art (str) - waste type
  - datum (date) - collection date
  - delta_days (int) - days until collection
  - day (str) - German day name
- **API**: Uses MHEG waste management API with caching (15 minutes)
- **Configuration Notes**: Address is hardcoded in mheg.py (str_name, str_hnr, fra_strase)

#### 6. Vertretungsplan (School Substitution Schedule)
- **Status**: ✅ Complete
- **URL**: `/vertretungsplan/`
- **View**: `core.views.vertretungsplan` (`core/views.py:87-115`)
- **Template**: `core/templates/core/vertretungsplan.html`
- **Repository**: `family_intranet/repositories/gymbroich.py`
- **Description**: Displays school substitution schedule for Mattis at Gymnasium Broich
- **Features**:
  - Fetches substitution schedule from Gymnasium Broich API
  - Date selector dropdown to view different days
  - Tab-based interface with two views:
    - **Mattis Tab**: Shows only substitutions relevant to Mattis's class (calculated dynamically)
    - **Gesamte Schule Tab**: Shows all substitutions for the entire school
  - Displays lesson number, subject, teacher, room information
  - Color-coded badges for canceled vs. substituted lessons
  - Shows general information and announcements
  - Displays timestamp of last update
  - Error handling for API/network issues
  - Responsive Bootstrap layout with card-based design
  - Mattis tab as default view
- **Dependencies**: requests, babel, pydantic, cachetools
- **Data Model**: `Vertretungsplan` and `VertretungsplanEvent` Pydantic BaseModels with fields:
  - VertretungsplanEvent: classes, lessons, subject, teacher, room, comment, canceled (with previous values)
  - Vertretungsplan: datum, timestamp_aktualisiert, infos, events
- **API**: Uses Gymnasium Broich Vertretungsplan API with caching (1 minute)
- **Configuration Notes**:
  - MATTIS_YEAR_STARTED = 2023
  - MATTIS_CLASS_SUFFIX = "B"
  - Class is calculated dynamically based on current date

#### 7. Pi-hole Control
- **Status**: ✅ Complete
- **URLs**:
  - `/pihole/status/` (GET endpoint for current status)
  - `/pihole/disable/` (POST endpoint to disable blocking)
- **Views**:
  - `core.views.pihole_status` (`core/views.py:122-139`)
  - `core.views.pihole_disable` (`core/views.py:142-162`)
- **Repository**: `family_intranet/repositories/pihole.py`
- **Description**: Remote control for Pi-hole DNS blocking (disables blocking for 5 minutes)
- **Features**:
  - Button on home page to disable DNS blocking temporarily
  - Supports multiple Pi-hole servers (primary + optional backup)
  - Disables blocking on both servers simultaneously
  - Backup server failure doesn't prevent primary from working
  - Communicates with Pi-hole v6 API
  - Disables blocking for exactly 5 minutes (300 seconds)
  - Live countdown timer showing time until blocking re-enables
  - Timer automatically loads on page refresh if blocking is already disabled
  - HTMX-powered async request with loading indicator
  - Success/error message display with auto-dismiss (10 seconds)
  - JSON response with blocking status and timer information
  - Error handling for network/connection issues
  - Uses session-based authentication with password (configured via environment variables)
  - Session ID (sid) and CSRF token passed via headers
- **Dependencies**: requests, pydantic
- **Data Model**: `BlockingStatus` Pydantic BaseModel with fields:
  - blocking (bool) - current blocking state
  - timer (int | None) - seconds until blocking re-enables
- **API Endpoints**:
  - GET `/api/dns/blocking` - get current blocking status
  - POST `/api/dns/blocking` - enable/disable blocking with optional timer
- **Configuration**:
  - Primary Pi-hole:
    - `PIHOLE_PRIMARY_URL` environment variable (default: "http://rasp2.local")
    - `PIHOLE_PRIMARY_PASSWORD` environment variable (required for authentication)
  - Backup Pi-hole (optional):
    - `PIHOLE_BACKUP_URL` environment variable
    - `PIHOLE_BACKUP_PASSWORD` environment variable
  - Legacy environment variables (backwards compatible):
    - `PIHOLE_URL` (maps to PRIMARY_URL)
    - `PIHOLE_PASSWORD` (maps to PRIMARY_PASSWORD)
  - SSL verification disabled (self-signed certificate)
  - Uses session-based authentication (POST to `/api/auth` with password)
- **UI Integration**:
  - Pi-hole control section on home page with warning button
  - JavaScript event handler for HTMX response processing
  - Bootstrap alert messages for feedback

### Development Commands
- **Run Server**: `uv run python manage.py runserver`
- **Add Dependencies**: `uv add package_name`
- **Run Migrations**: `uv run python manage.py migrate`
- **Create Superuser**: `uv run python manage.py createsuperuser`
- **Collect Static**: `uv run python manage.py collectstatic`

### Code Quality Commands
- **Lint Code**: `uv run ruff check .`
- **Format Code**: `uv run ruff format .`
- **Fix Linting Issues**: `uv run ruff check . --fix`
- **Type Check**: `uv run ty check .`

### ⚠️ IMPORTANT: Code Quality Workflow
**ALWAYS run these commands after making code changes:**
1. `uv run ruff format .` (format code)
2. `uv run ruff check . --fix` (fix linting issues)
3. `uv run ty check .` (type check)

**All three must pass before considering changes complete!**

### Next Steps (Future Implementation)
1. **Information Hub**: APIs and additional data sources
2. **PostgreSQL Setup**: Replace SQLite with PostgreSQL
3. **User Authentication**: Family member login system
4. **Admin Interface**: Django admin customization for family data
5. **Data Caching**: Cache scraped sports data to reduce API calls
6. **Automatic Updates**: Background task to refresh sports data periodically

### Technical Notes
- **HTMX Target**: `#main-content` div for dynamic updates (not used on handball page)
- **Bootstrap Components**: Used cards, navbar, buttons, grid system, badges
- **Loading Indicators**: HTMX loading spinner with CSS transitions
- **Responsive Design**: Mobile-first approach with Bootstrap classes
- **Color Scheme**: Dark navbar, gradient hero, light features section
- **Code Quality**:
  - Ruff configured for Django projects with comprehensive rules
  - Per-file ignores for Django-generated files (manage.py, migrations)
  - DTZ007 ignored for handballnordrhein.py, fussballde.py, core/views.py (date-only parsing from form inputs)
  - mheg.py: DTZ005, DTZ011, N815, E501, PLR2004 ignored (legacy code)
  - gymbroich.py: DTZ005, DTZ007, N815, E501, S113, SIM210, PLW2901, PLR2004 ignored (API naming conventions)
  - pihole.py: TRY003, EM101, EM102 ignored (exception message formatting)
  - google_calendar.py: SIM102, RET504, TRY003, EM102, DTZ011, B905, PLW2901, PLW0127, C416 ignored (legacy code patterns)
  - .github files excluded from linting
- **Formatting**: Double quotes, 88 character line length, isort integration
- **Type Checking**:
  - ty (Astral's ultra-fast type checker) configured for Python 3.13
  - Excludes: migrations, manage.py, .venv, .github, mheg.py (legacy code), pihole.py (requests type stubs), google_calendar.py (external library type issues)
- **Error Handling**: Specific exception types (ConnectionError, TimeoutError, ValueError)
- **Web Scraping**: BeautifulSoup4 for HTML parsing, requests for HTTP calls

## Commands
*(To be added as we discover project-specific commands)*