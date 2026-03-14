"""Pushover push notification integration."""

import requests
import requests.exceptions

from family_intranet import settings


class PushoverConfig:
    API_TOKEN = settings.PUSHOVER_API_TOKEN
    USER_KEY = settings.PUSHOVER_USER_KEY
    API_URL = "https://api.pushover.net/1/messages.json"
    TIMEOUT = 10


class PushoverRepository:
    """Repository for sending Pushover push notifications."""

    def send_notification(self, message: str, title: str | None = None) -> None:
        """Send a push notification via Pushover.

        Raises:
            ConnectionError: If connection to Pushover fails
            TimeoutError: If request times out
            ValueError: If API returns an error response
        """
        payload = {
            "token": PushoverConfig.API_TOKEN,
            "user": PushoverConfig.USER_KEY,
            "message": message,
        }
        if title:
            payload["title"] = title

        try:
            response = requests.post(
                PushoverConfig.API_URL,
                json=payload,
                timeout=PushoverConfig.TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("status") != 1:
                errors = data.get("errors", "Unknown error")
                msg = f"Pushover API error: {errors}"
                raise ValueError(msg)
        except requests.exceptions.ConnectionError as e:
            msg = "Failed to connect to Pushover API"
            raise ConnectionError(msg) from e
        except requests.exceptions.Timeout as e:
            msg = "Pushover API request timed out"
            raise TimeoutError(msg) from e
        except requests.exceptions.HTTPError as e:
            msg = f"Pushover API HTTP error: {e}"
            raise ValueError(msg) from e
        except requests.exceptions.RequestException as e:
            msg = f"Pushover API request failed: {e}"
            raise ValueError(msg) from e
