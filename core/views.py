from datetime import date

from django.shortcuts import render

from family_intranet.repositories.fussballde import (
    get_e2_junioren_home_url,
    get_erik_e2_junioren_next_games,
    get_speldorf_next_home_games,
    get_vfb_speldorf_home_url,
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


def home(request):
    return render(request, "core/home.html")


def handball_games(request):
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
        return render(request, "core/handball_games.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/handball_games.html", context)


def football_games(request):
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
        return render(request, "core/football_games.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/football_games.html", context)


def muelltermine(request):
    try:
        termine = get_muelltermine_for_home()
        wertstoffhof = get_wertstoffhof_oeffnungszeiten()
        context = {"termine": termine, "wertstoffhof": wertstoffhof}
        return render(request, "core/muelltermine.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/muelltermine.html", context)


def vertretungsplan(request):
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
        return render(request, "core/vertretungsplan.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/vertretungsplan.html", context)
