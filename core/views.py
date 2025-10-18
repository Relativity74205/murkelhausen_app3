from django.shortcuts import render

from family_intranet.repositories.fussballde import (
    get_e2_junioren_home_url,
    get_erik_e2_junioren_next_games,
    get_speldorf_next_home_games,
    get_vfb_speldorf_home_url,
)
from family_intranet.repositories.handballnordrhein import (
    get_d_jugend_gruppe_url,
    get_d_jugend_url,
    get_djk_saarn_d_jugend,
    get_djk_saarn_erste_herren,
    get_erste_herren,
    get_erste_herren_gruppe_url,
)
from family_intranet.repositories.mheg import get_muelltermine_for_home


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
        context = {"termine": termine}
        return render(request, "core/muelltermine.html", context)
    except (ConnectionError, TimeoutError, ValueError) as e:
        context = {"error": str(e)}
        return render(request, "core/muelltermine.html", context)
