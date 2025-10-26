"""Context processors for the core app."""

from django.conf import settings


def htmx_timeout(request):  # noqa: ARG001
    """Add HTMX_TIMEOUT to all template contexts."""
    return {"HTMX_TIMEOUT": settings.HTMX_TIMEOUT}
