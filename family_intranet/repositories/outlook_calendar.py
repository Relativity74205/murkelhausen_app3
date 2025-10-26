"""Outlook Calendar ICS integration for work appointments."""

import logging
from datetime import UTC, date, datetime, timedelta

import pytz
import requests
from icalendar import Calendar
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class WorkAppointment(BaseModel):
    """Work appointment from Outlook calendar."""

    event_name: str
    start_timestamp: datetime
    end_timestamp: datetime
    start_date: date
    end_date: date
    start_time: str
    end_time: str
    description: str | None
    location: str | None
    is_whole_day: bool
    is_recurring: bool
    is_tentative: bool


def fetch_work_calendar(ics_url: str, days_ahead: int = 7) -> list[WorkAppointment]:
    """
    Fetch work appointments from Outlook ICS calendar.

    Args:
        ics_url: URL to the ICS calendar feed
        days_ahead: Number of days to fetch (default: 7 for one week)

    Returns:
        List of WorkAppointment objects sorted by start time

    Raises:
        ConnectionError: If fetching the calendar fails
        ValueError: If parsing the ICS data fails
    """
    try:
        # Fetch ICS calendar
        response = requests.get(ics_url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.exception("Failed to fetch Outlook calendar")
        raise ConnectionError(f"Failed to fetch Outlook calendar: {e}") from e

    try:
        # Parse ICS data
        cal = Calendar.from_ical(response.content)
    except Exception as e:
        logger.exception("Failed to parse ICS calendar data")
        raise ValueError(f"Failed to parse ICS calendar data: {e}") from e

    # Calculate date range
    berlin_tz = pytz.timezone("Europe/Berlin")
    today = datetime.now(UTC).date()
    end_date = today + timedelta(days=days_ahead)

    appointments = []

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        try:
            # Extract event data
            summary = str(component.get("summary", "Kein Titel"))

            # Handle start time
            dtstart = component.get("dtstart")
            if dtstart is None:
                continue
            start = dtstart.dt

            # Handle end time
            dtend = component.get("dtend")
            if dtend:
                end = dtend.dt
            else:
                # If no end time, assume 1 hour duration
                end = (
                    start + timedelta(hours=1) if isinstance(start, datetime) else start
                )

            # Check if whole day event
            is_whole_day = isinstance(start, date) and not isinstance(start, datetime)

            # Convert to datetime if needed and convert to Berlin timezone
            if is_whole_day:
                start_dt = datetime.combine(start, datetime.min.time(), tzinfo=UTC)
                end_dt = datetime.combine(end, datetime.min.time(), tzinfo=UTC)
            else:
                # Ensure timezone aware
                if start.tzinfo is None:
                    start_dt = start.replace(tzinfo=UTC)
                else:
                    start_dt = start.astimezone(UTC)

                if end.tzinfo is None:
                    end_dt = end.replace(tzinfo=UTC)
                else:
                    end_dt = end.astimezone(UTC)

            # Filter by date range
            event_date = start_dt.date()
            if event_date < today or event_date > end_date:
                continue

            # Extract additional fields
            description = component.get("description")
            if description:
                description = str(description).strip()

            location = component.get("location")
            if location:
                location = str(location).strip()

            # Check if recurring
            is_recurring = component.get("rrule") is not None

            # Check appointment status (PARTSTAT or STATUS)
            # STATUS can be: TENTATIVE, CONFIRMED, CANCELLED
            # For Outlook "Unter Vorbehalt" is TENTATIVE
            status = component.get("status")
            is_tentative = str(status).upper() == "TENTATIVE" if status else False

            # Format times in Berlin timezone
            if is_whole_day:
                start_time_str = "Ganztägig"
                end_time_str = ""
            else:
                # Convert to Berlin timezone for display
                start_berlin = start_dt.astimezone(berlin_tz)
                end_berlin = end_dt.astimezone(berlin_tz)
                start_time_str = start_berlin.strftime("%H:%M")
                end_time_str = end_berlin.strftime("%H:%M")

            appointment = WorkAppointment(
                event_name=summary,
                start_timestamp=start_dt,
                end_timestamp=end_dt,
                start_date=start_dt.date(),
                end_date=end_dt.date(),
                start_time=start_time_str,
                end_time=end_time_str,
                description=description,
                location=location,
                is_whole_day=is_whole_day,
                is_recurring=is_recurring,
                is_tentative=is_tentative,
            )

            appointments.append(appointment)

        except Exception as e:
            logger.exception("Failed to parse calendar event: %s", e)
            continue

    # Sort by start time
    appointments.sort(key=lambda x: x.start_timestamp)

    return appointments
