from django.conf import settings
from garminconnect import Garmin

from family_intranet.jobs.garmin.auth import get_auth_token


def get_garmin_client() -> Garmin:
    garmin = Garmin()
    try:
        garmin.login(settings.GARMIN_AUTH_TOKEN_PATH)
    except FileNotFoundError:
        get_auth_token()
        garmin.login(settings.GARMIN_AUTH_TOKEN_PATH)
    return garmin
