from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("handball/", views.handball_games, name="handball_games"),
    path("football/", views.football_games, name="football_games"),
    path("muell/", views.muelltermine, name="muelltermine"),
]
