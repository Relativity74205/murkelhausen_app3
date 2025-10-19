"""Pi-hole API integration for DNS blocking control."""

import os
from datetime import UTC, datetime, timedelta

import requests
from pydantic import BaseModel


class PiHoleConfig:
    # Primary Pi-hole
    PRIMARY_URL = os.getenv("PIHOLE_PRIMARY_URL", "http://rasp1.lan")
    PRIMARY_PASSWORD = os.getenv("PIHOLE_PRIMARY_PASSWORD", "")

    # Backup Pi-hole
    BACKUP_URL = os.getenv("PIHOLE_BACKUP_URL", "http://192.168.1.28")  # rasp2.lan doesn't work via mDNS at the moment for some reason
    BACKUP_PASSWORD = os.getenv("PIHOLE_BACKUP_PASSWORD", "")

    TIMEOUT = 10


class BlockingStatus(BaseModel):
    """Pi-hole blocking status response."""

    blocking: bool
    timer: float | None = None


class PiHoleSession(BaseModel):
    sid: str
    csrf: str
    valid_until: datetime


class PiHoleRepository:
    """Repository for interacting with Pi-hole API."""

    def __init__(self, base_url: str | None = None, password: str | None = None):
        """Initialize Pi-hole repository.
        """
        self.base_url = base_url
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.pi_hole_session: PiHoleSession | None = None

    def _authenticate(self) -> None:
        """Authenticate with Pi-hole using password to establish session.

        Returns session ID.

        Raises:
            ConnectionError: If connection to Pi-hole fails
            TimeoutError: If request times out
            ValueError: If authentication fails
        """
        if (
            self.pi_hole_session
            and self.pi_hole_session.valid_until > datetime.now(tz=UTC)
        ):
            return

        try:
            response = self.session.post(
                f"{self.base_url}/api/auth",
                json={"password": self.password},
                timeout=PiHoleConfig.TIMEOUT,
                verify=False,
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("session", {}).get("valid", False):
                raise ValueError("Authentication failed: Invalid credentials")

            session = data["session"]
            self.pi_hole_session = PiHoleSession(
                sid=session["sid"],
                csrf=session["csrf"],
                valid_until=datetime.now(tz=UTC)
                + timedelta(seconds=session["validity"]),
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to Pi-hole at {self.base_url}"
            ) from e
        except requests.exceptions.Timeout as e:
            raise TimeoutError("Pi-hole API request timed out") from e
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Authentication failed: {e}") from e
        except (requests.exceptions.RequestException, KeyError) as e:
            raise ValueError(f"Invalid response from Pi-hole API: {e}") from e

    def get_blocking_status(self) -> BlockingStatus:
        """Get current DNS blocking status.

        Raises:
            ConnectionError: If connection to Pi-hole fails
            TimeoutError: If request times out
            ValueError: If API returns invalid response
        """
        self._authenticate()
        headers = {
            "X-FTL-SID": self.pi_hole_session.sid,
            "X-FTL-CSRF": self.pi_hole_session.csrf,
        }

        try:
            response = self.session.get(
                f"{self.base_url}/api/dns/blocking",
                headers=headers,
                timeout=PiHoleConfig.TIMEOUT,
                verify=False,
            )
            response.raise_for_status()
            data = response.json()
            return BlockingStatus(
                blocking=data["blocking"] == "enabled", timer=data.get("timer")
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to Pi-hole at {self.base_url}"
            ) from e
        except requests.exceptions.Timeout as e:
            raise TimeoutError("Pi-hole API request timed out") from e
        except (requests.exceptions.RequestException, KeyError) as e:
            raise ValueError(f"Invalid response from Pi-hole API: {e}") from e

    def disable_blocking(self, duration_seconds: int = 300) -> BlockingStatus:
        """Disable DNS blocking for a specified duration.

        Raises:
            ConnectionError: If connection to Pi-hole fails
            TimeoutError: If request times out
            ValueError: If API returns invalid response
        """
        self._authenticate()
        headers = {
            "X-FTL-SID": self.pi_hole_session.sid,
            "X-FTL-CSRF": self.pi_hole_session.csrf,
        }

        try:
            response = self.session.post(
                f"{self.base_url}/api/dns/blocking",
                headers=headers,
                json={"blocking": False, "timer": duration_seconds},
                timeout=PiHoleConfig.TIMEOUT,
                verify=False,
            )
            response.raise_for_status()
            data = response.json()
            return BlockingStatus(
                blocking=data["blocking"] == "enabled", timer=data.get("timer")
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to Pi-hole at {self.base_url}"
            ) from e
        except requests.exceptions.Timeout as e:
            raise TimeoutError("Pi-hole API request timed out") from e
        except (requests.exceptions.RequestException, KeyError) as e:
            raise ValueError(f"Invalid response from Pi-hole API: {e}") from e



class MultiPiHoleRepository:
    """Repository for managing multiple Pi-hole instances (primary and backup)."""

    def __init__(self):
        """Initialize multi Pi-hole repository with primary and backup servers."""
        self.primary = PiHoleRepository(
            base_url=PiHoleConfig.PRIMARY_URL,
            password=PiHoleConfig.PRIMARY_PASSWORD,
        )

        self.backup = PiHoleRepository(
            base_url=PiHoleConfig.BACKUP_URL,
            password=PiHoleConfig.BACKUP_PASSWORD,
        )

    def get_blocking_status(self) -> BlockingStatus:
        """Get blocking status from primary Pi-hole.

        Raises:
            ConnectionError: If connection fails
            TimeoutError: If request times out
            ValueError: If API returns invalid response
        """
        return self.primary.get_blocking_status()

    def disable_blocking(self, duration_seconds: int = 300) -> BlockingStatus:
        """Disable blocking on both primary and backup Pi-hole servers.

        Raises:
            ConnectionError: If connection fails
            TimeoutError: If request times out
            ValueError: If API returns invalid response
        """
        primary_blocking_status = self.primary.disable_blocking(duration_seconds)
        secondary_blocking_status = self.backup.disable_blocking(duration_seconds)

        if primary_blocking_status.blocking is not False and primary_blocking_status.blocking != secondary_blocking_status.blocking:
            raise ValueError("Failed to disable blocking on one of the Pi-hole servers")

        return primary_blocking_status


# if __name__ == "__main__":
#     repo = MultiPiHoleRepository()
#     status = repo.get_blocking_status()
#     print(f"Blocking: {status.blocking}, Timer: {status.timer}")
#
#     status = repo.disable_blocking(duration_seconds=300)
#     print(f"Blocking: {status.blocking}, Timer: {status.timer}")