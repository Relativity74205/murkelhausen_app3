import zoneinfo
from datetime import UTC, datetime


def _get_wind_direction(degrees: int) -> str:
    if degrees is None:
        return ""
    if degrees < 22.5:
        return "N"
    if degrees < 67.5:
        return "NO"
    if degrees < 112.5:
        return "O"
    if degrees < 157.5:
        return "SO"
    if degrees < 202.5:
        return "S"
    if degrees < 247.5:
        return "SW"
    if degrees < 292.5:
        return "W"
    if degrees < 337.5:
        return "NW"
    return "N"


def _get_moon_phase_string(moon_phase: float) -> str:
    if moon_phase < 0.025:
        s = "Neumond"
    elif moon_phase < 0.225:
        s = "zunehmende Sichel"
    elif moon_phase < 0.275:
        s = "erstes Viertel"
    elif moon_phase < 0.475:
        s = "zunehmender Halbmond"
    elif moon_phase < 0.525:
        s = "Neumond"
    elif moon_phase < 0.725:
        s = "abnehmender Halbmond"
    elif moon_phase < 0.775:
        s = "letztes Viertel"
    elif moon_phase < 0.975:
        s = "abnehmende Sichel"
    else:
        s = "Neumond"

    return s + f" ({moon_phase * 100:.0f} %)"


def _get_uv_index_category(uv_index: float) -> str:
    if uv_index < 3:
        return "keine bis gering"
    if uv_index < 6:
        return "mittel"
    if uv_index < 8:
        return "hoch"
    if uv_index < 11:
        return "sehr hoch"
    return "extrem hoch"


def _unix_timestamp_to_met_hour(unix_timestamp: int) -> str:
    return (
        datetime.fromtimestamp(unix_timestamp, tz=UTC)
        .astimezone(zoneinfo.ZoneInfo("Europe/Berlin"))
        .strftime("%H:%M")
    )


def _unix_timestamp_to_met_timestamp(unix_timestamp: int) -> str:
    return (
        datetime.fromtimestamp(unix_timestamp, tz=UTC)
        .astimezone(zoneinfo.ZoneInfo("Europe/Berlin"))
        .strftime("%d.%m.%Y %H:%M")
    )
