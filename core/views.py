import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime

import pytz
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from gcsa.event import Event

from family_intranet.repositories.fussballde import (
    get_e2_junioren_home_url,
    get_erik_e2_junioren_next_games,
    get_speldorf_next_home_games,
    get_vfb_speldorf_home_url,
)
from family_intranet.repositories.google_calendar import (
    create_appointment,
    delete_appointment,
    get_list_of_appointments,
)
from family_intranet.repositories.gymbroich import (
    get_vertretungsplan,
    get_vertretungsplan_dates,
    get_vertretungsplan_mattis,
)
from family_intranet.repositories.handballnordrhein import (
    get_d_jugend_gruppe_url,
    get_d_jugend_url,
    get_djk_saarn_d_jugend,
    get_djk_saarn_erste_herren,
    get_erste_herren,
    get_erste_herren_gruppe_url,
)
from family_intranet.repositories.mheg import (
    get_muelltermine_for_home,
    get_wertstoffhof_oeffnungszeiten,
)
from family_intranet.repositories.owm import get_weather_data_muelheim
from family_intranet.repositories.pihole import MultiPiHoleRepository
from family_intranet.settings import GOOGLE_CALENDAR_SETTINGS


def home(request):
    return render(request, "core/home.html")


def handball_games(request):
    # Initial page load - just show loading placeholder
    return render(request, "core/handball_games.html")


def handball_games_data(request):
    # Async data loading for HTMX
    try:
        d_jugend_games = get_djk_saarn_d_jugend()
        erste_herren_games = get_djk_saarn_erste_herren()
        d_jugend_url = get_d_jugend_url()
        d_jugend_gruppe_url = get_d_jugend_gruppe_url()
        erste_herren_url = get_erste_herren()
        erste_herren_gruppe_url = get_erste_herren_gruppe_url()

        context = {
            "d_jugend_games": d_jugend_games,
            "erste_herren_games": erste_herren_games,
            "d_jugend_url": d_jugend_url,
            "d_jugend_gruppe_url": d_jugend_gruppe_url,
            "erste_herren_url": erste_herren_url,
            "erste_herren_gruppe_url": erste_herren_gruppe_url,
        }
        return render(request, "core/handball_games_content.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/handball_games_content.html", context)


def football_games(request):
    # Initial page load - just show loading placeholder
    return render(request, "core/football_games.html")


def football_games_data(request):
    # Async data loading for HTMX
    try:
        e2_junioren_games = get_erik_e2_junioren_next_games()
        speldorf_home_games = get_speldorf_next_home_games()
        e2_junioren_url = get_e2_junioren_home_url()
        vfb_speldorf_url = get_vfb_speldorf_home_url()

        context = {
            "e2_junioren_games": e2_junioren_games,
            "speldorf_home_games": speldorf_home_games,
            "e2_junioren_url": e2_junioren_url,
            "vfb_speldorf_url": vfb_speldorf_url,
        }
        return render(request, "core/football_games_content.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/football_games_content.html", context)


def muelltermine(request):
    # Initial page load - just show loading placeholder
    return render(request, "core/muelltermine.html")


def muelltermine_data(request):
    # Async data loading for HTMX
    try:
        termine = get_muelltermine_for_home()
        wertstoffhof = get_wertstoffhof_oeffnungszeiten()
        context = {"termine": termine, "wertstoffhof": wertstoffhof}
        return render(request, "core/muelltermine_content.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/muelltermine_content.html", context)


def vertretungsplan(request):
    # Initial page load - just show loading placeholder
    return render(request, "core/vertretungsplan.html")


def vertretungsplan_data(request):
    # Async data loading for HTMX
    try:
        # Get available dates
        available_dates = get_vertretungsplan_dates()

        # Get the selected date from query params, default to first available date
        selected_date_str = request.GET.get("date")
        if selected_date_str:
            selected_date = date.fromisoformat(selected_date_str)
        else:
            selected_date = available_dates[0] if available_dates else None

        # Get the vertretungsplan for the selected date
        vertretungsplan_mattis = None
        vertretungsplan_full = None
        if selected_date:
            vertretungsplan_mattis = get_vertretungsplan_mattis(selected_date)
            vertretungsplan_full = get_vertretungsplan(selected_date)

        context = {
            "available_dates": available_dates,
            "selected_date": selected_date,
            "vertretungsplan_mattis": vertretungsplan_mattis,
            "vertretungsplan_full": vertretungsplan_full,
        }
        return render(request, "core/vertretungsplan_content.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/vertretungsplan_content.html", context)


def pihole_status(request):  # noqa: ARG001
    """Get current Pi-hole blocking status."""
    logger = logging.getLogger(__name__)

    try:
        repo = MultiPiHoleRepository()
        status = repo.get_blocking_status()

        return JsonResponse(
            {
                "success": True,
                "blocking": status.blocking,
                "timer": int(status.timer) if status.timer else None,
            }
        )
    except (ConnectionError, TimeoutError, ValueError) as e:
        logger.error(f"Pi-hole status error: {e}", exc_info=True)
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_POST
def pihole_disable(request):  # noqa: ARG001
    """Disable Pi-hole DNS blocking for 5 minutes."""
    logger = logging.getLogger(__name__)

    try:
        repo = MultiPiHoleRepository()
        logger.info("Attempting to disable Pi-hole blocking on all servers")
        status = repo.disable_blocking(duration_seconds=300)  # 5 minutes

        return JsonResponse(
            {
                "success": True,
                "blocking": status.blocking,
                "timer": int(status.timer) if status.timer else None,
                "message": "DNS blocking disabled for 5 minutes",
            }
        )
    except (ConnectionError, TimeoutError, ValueError) as e:
        logger.error(f"Pi-hole error: {e}", exc_info=True)
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def weather(request):
    try:
        weather_data, error = get_weather_data_muelheim()
        context = {"error": error} if error else {"weather": weather_data}
        return render(request, "core/weather.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/weather.html", context)


def calendar(request):
    # Initial page load - just show loading placeholder
    return render(request, "core/calendar.html")


def calendar_data(request):
    # Async data loading for HTMX
    try:
        # Fetch appointments from all calendars in parallel for better performance
        all_appointments = []

        # Use ThreadPoolExecutor to fetch calendars concurrently
        with ThreadPoolExecutor(max_workers=6) as executor:
            # Submit all calendar fetch tasks
            calendars = GOOGLE_CALENDAR_SETTINGS.calendars.items()
            future_to_calendar = {
                executor.submit(
                    get_list_of_appointments,
                    calendar_id=calendar_id,
                    calendar_name=calendar_name,
                    amount_of_days_to_show=7,
                ): calendar_name
                for calendar_name, calendar_id in calendars
            }

            # Collect results as they complete
            for future in as_completed(future_to_calendar):
                calendar_name = future_to_calendar[future]
                try:
                    appointments = future.result()
                    all_appointments.extend(appointments)
                except Exception as e:
                    # Log error but continue with other calendars
                    logger = logging.getLogger(__name__)
                    logger.error(
                        f"Error fetching calendar '{calendar_name}': {e}",
                        exc_info=True,
                    )

        # Sort all appointments by start timestamp
        all_appointments.sort(key=lambda x: x.start_timestamp)

        # Group appointments by date for better display
        appointments_by_date = defaultdict(list)
        for appointment in all_appointments:
            appointments_by_date[appointment.start_date].append(appointment)

        # Convert to sorted list of (date, appointments) tuples
        grouped_appointments = sorted(appointments_by_date.items())

        context = {
            "grouped_appointments": grouped_appointments,
            "all_appointments": all_appointments,
        }
        return render(request, "core/calendar_content.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/calendar_content.html", context)


@require_POST
def calendar_create(request):
    """Create a new appointment in the selected calendar."""
    logger = logging.getLogger(__name__)

    try:
        # Get form data
        calendar_name = request.POST.get("calendar")
        event_name = request.POST.get("event_name")
        start_date_str = request.POST.get("start_date")
        start_time_str = request.POST.get("start_time")
        end_date_str = request.POST.get("end_date")
        end_time_str = request.POST.get("end_time")
        is_whole_day = request.POST.get("is_whole_day") == "on"
        description = request.POST.get("description", "")

        # Validate required fields
        if not all([calendar_name, event_name, start_date_str, end_date_str]):
            return JsonResponse(
                {"success": False, "error": "Bitte alle Pflichtfelder ausfüllen"},
                status=400,
            )

        # Get calendar ID from settings
        if calendar_name not in GOOGLE_CALENDAR_SETTINGS.calendars:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Kalender '{calendar_name}' nicht gefunden",
                },
                status=400,
            )

        calendar_id = GOOGLE_CALENDAR_SETTINGS.calendars[calendar_name]

        # Parse dates
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Create start and end datetime objects
        berlin_tz = pytz.timezone("Europe/Berlin")

        if is_whole_day or not start_time_str:
            # All-day event
            start = start_date
            end = end_date
        else:
            # Timed event
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            start = berlin_tz.localize(datetime.combine(start_date, start_time))

            if end_time_str:
                end_time = datetime.strptime(end_time_str, "%H:%M").time()
                end = berlin_tz.localize(datetime.combine(end_date, end_time))
            else:
                # Default to 1 hour duration
                end = start.replace(hour=start.hour + 1)

        # Create Event object
        event = Event(
            summary=event_name,
            start=start,
            end=end,
            description=description if description else None,
        )

        # Create the appointment
        logger.info(
            f"Creating appointment '{event_name}' in calendar '{calendar_name}'"
        )
        create_appointment(event, calendar_id)

        return JsonResponse(
            {
                "success": True,
                "message": f"Termin '{event_name}' wurde erfolgreich erstellt",
            }
        )

    except ValueError as e:
        logger.error(f"Validation error creating appointment: {e}", exc_info=True)
        return JsonResponse(
            {"success": False, "error": f"Ungültige Eingabe: {e!s}"}, status=400
        )
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error creating appointment: {e}", exc_info=True)
        return JsonResponse(
            {"success": False, "error": "Netzwerkfehler beim Erstellen des Termins"},
            status=500,
        )
    except Exception as e:
        logger.error(f"Error creating appointment: {e}", exc_info=True)
        return JsonResponse(
            {"success": False, "error": f"Fehler beim Erstellen: {e!s}"}, status=500
        )


@require_POST
def calendar_delete(request):
    """Delete an appointment from a calendar."""
    logger = logging.getLogger(__name__)

    try:
        # Get form data
        appointment_id = request.POST.get("appointment_id")
        calendar_name = request.POST.get("calendar_name")

        # Validate required fields
        if not all([appointment_id, calendar_name]):
            return JsonResponse(
                {"success": False, "error": "Fehlende Pflichtfelder"}, status=400
            )

        # Get calendar ID from settings
        if calendar_name not in GOOGLE_CALENDAR_SETTINGS.calendars:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Kalender '{calendar_name}' nicht gefunden",
                },
                status=400,
            )

        calendar_id = GOOGLE_CALENDAR_SETTINGS.calendars[calendar_name]

        # Create Event object with minimal data for deletion
        # Event constructor requires summary/start, but not used for deletion
        event = Event(
            summary="",  # Dummy value, not used for deletion
            start=datetime.now(tz=pytz.UTC).date(),  # Dummy, not used
            event_id=appointment_id,
        )

        # Delete the appointment
        logger.info(
            f"Deleting appointment '{appointment_id}' from calendar '{calendar_name}'"
        )
        delete_appointment(event, calendar_id)

        return JsonResponse(
            {"success": True, "message": "Termin wurde erfolgreich gelöscht"}
        )

    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error deleting appointment: {e}", exc_info=True)
        return JsonResponse(
            {"success": False, "error": "Netzwerkfehler beim Löschen des Termins"},
            status=500,
        )
    except Exception as e:
        logger.error(f"Error deleting appointment: {e}", exc_info=True)
        return JsonResponse(
            {"success": False, "error": f"Fehler beim Löschen: {e!s}"}, status=500
        )
