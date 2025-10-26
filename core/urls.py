from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("handball/", views.handball_games, name="handball_games"),
    path("handball/data/", views.handball_games_data, name="handball_games_data"),
    path("football/", views.football_games, name="football_games"),
    path("football/data/", views.football_games_data, name="football_games_data"),
    path("muell/", views.muelltermine, name="muelltermine"),
    path("muell/data/", views.muelltermine_data, name="muelltermine_data"),
    path("vertretungsplan/", views.vertretungsplan, name="vertretungsplan"),
    path(
        "vertretungsplan/data/", views.vertretungsplan_data, name="vertretungsplan_data"
    ),
    path("weather/", views.weather, name="weather"),
    path("pihole/status/", views.pihole_status, name="pihole_status"),
    path("pihole/disable/", views.pihole_disable, name="pihole_disable"),
    path("calendar/", views.calendar, name="calendar"),
    path("calendar/data/", views.calendar_data, name="calendar_data"),
    path("calendar/create/", views.calendar_create, name="calendar_create"),
    path("calendar/delete/", views.calendar_delete, name="calendar_delete"),
]
