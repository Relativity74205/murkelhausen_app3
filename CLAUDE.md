# Project: Murkelhausen App 3

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
- **Core URLs**: `core/urls.py` (home view)
- **Home View**: `core/views.py` (renders home.html)
- **Home Template**: `core/templates/core/home.html` (Bootstrap + HTMX)
- **Dependencies**: `pyproject.toml` (managed by uv)

### Current Implementation
- **Home Page**: Fully functional with Bootstrap 5.3 styling
- **Navigation**: Responsive navbar with HTMX-enabled links
- **Features Showcased**: Calendar, Sports Schedule, Information Hub
- **HTMX Integration**: Loading indicators and dynamic content areas
- **Styling**: Bootstrap CDN + custom CSS for hero section and cards

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
2. **Sports Scraping**: Web scraping for football/handball games
3. **Information Hub**: APIs and additional data sources
4. **PostgreSQL Setup**: Replace SQLite with PostgreSQL
5. **User Authentication**: Family member login system
6. **Admin Interface**: Django admin customization for family data

### Technical Notes
- **HTMX Target**: `#main-content` div for dynamic updates
- **Bootstrap Components**: Used cards, navbar, buttons, grid system
- **Loading Indicators**: HTMX loading spinner with CSS transitions
- **Responsive Design**: Mobile-first approach with Bootstrap classes
- **Color Scheme**: Dark navbar, gradient hero, light features section
- **Code Quality**: Ruff configured for Django projects with comprehensive rules
- **Formatting**: Double quotes, 88 character line length, isort integration
- **Type Checking**: ty (Astral's ultra-fast type checker) configured for Python 3.13

## Commands
*(To be added as we discover project-specific commands)*