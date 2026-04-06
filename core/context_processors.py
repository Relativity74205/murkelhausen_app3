"""Context processors for the core app."""

import tomllib
from pathlib import Path

from django.conf import settings

with (Path(__file__).resolve().parent.parent / "pyproject.toml").open("rb") as _f:
    _APP_VERSION: str = tomllib.load(_f)["project"]["version"]


def htmx_timeout(request):  # noqa: ARG001
    """Add HTMX_TIMEOUT to all template contexts."""
    return {
        "HTMX_TIMEOUT": settings.HTMX_TIMEOUT,
        "TASKS_REFRESH_INTERVAL": settings.TASKS_REFRESH_INTERVAL,
        "APP_VERSION": _APP_VERSION,
    }
