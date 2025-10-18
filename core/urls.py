from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("handball/", views.handball_games, name="handball_games"),
]
