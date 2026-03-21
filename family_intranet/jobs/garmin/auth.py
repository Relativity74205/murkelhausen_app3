import garth
from django.conf import settings


def get_auth_token():
    garth.login(settings.GARMIN_EMAIL, settings.GARMIN_PASSWORD)
    garth.save(settings.GARMIN_AUTH_TOKEN_PATH)
