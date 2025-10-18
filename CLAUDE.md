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
- **Core URLs**: `core/urls.py` (home view, handball games)
- **Core Views**: `core/views.py` (home, handball_games)
- **Templates**:
  - `core/templates/core/home.html` (Bootstrap + HTMX)
  - `core/templates/core/handball_games.html` (Handball schedule display)
- **Repositories**: `family_intranet/repositories/handballnordrhein.py` (Web scraping)
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

#### 2. Handball Games Schedule
- **Status**: ✅ Complete
- **URL**: `/handball/`
- **View**: `core.views.handball_games` (`core/views.py:15-31`)
- **Template**: `core/templates/core/handball_games.html`
- **Repository**: `family_intranet/repositories/handballnordrhein.py`
- **Description**: Web scraping feature for DJK Saarn handball teams
- **Features**:
  - Scrapes game schedules from https://hnr-handball.liga.nu
  - Displays two teams: D-Jugend and Erste Herren
  - Shows game date, time, location, teams, and results
  - Links to official game reports (Spielbericht)
  - Badges for special cases: "Spielfrei" (free date), "Verlegt" (postponed)
  - Error handling for network issues
  - Responsive Bootstrap layout with card-based design
  - Direct links to league website for each team
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
1. **Calendar Integration**: Google Calendar API connection
2. **Football Scraping**: Web scraping for football games (similar to handball)
3. **Information Hub**: APIs and additional data sources
4. **PostgreSQL Setup**: Replace SQLite with PostgreSQL
5. **User Authentication**: Family member login system
6. **Admin Interface**: Django admin customization for family data
7. **Data Caching**: Cache scraped handball data to reduce API calls
8. **Automatic Updates**: Background task to refresh handball data periodically

### Technical Notes
- **HTMX Target**: `#main-content` div for dynamic updates (not used on handball page)
- **Bootstrap Components**: Used cards, navbar, buttons, grid system, badges
- **Loading Indicators**: HTMX loading spinner with CSS transitions
- **Responsive Design**: Mobile-first approach with Bootstrap classes
- **Color Scheme**: Dark navbar, gradient hero, light features section
- **Code Quality**:
  - Ruff configured for Django projects with comprehensive rules
  - Per-file ignores for Django-generated files (manage.py, migrations)
  - DTZ007 ignored for handballnordrhein.py (date-only parsing)
  - .github files excluded from linting
- **Formatting**: Double quotes, 88 character line length, isort integration
- **Type Checking**:
  - ty (Astral's ultra-fast type checker) configured for Python 3.13
  - Excludes: migrations, manage.py, .venv, .github
- **Error Handling**: Specific exception types (ConnectionError, TimeoutError, ValueError)
- **Web Scraping**: BeautifulSoup4 for HTML parsing, requests for HTTP calls

## Commands
*(To be added as we discover project-specific commands)*