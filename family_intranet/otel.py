import contextlib
import logging
import os
import time
from collections.abc import Generator

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

logger = logging.getLogger(__name__)

service_name: str = os.environ["OTEL_SERVICE_NAME"]
METRIC_PREFIX = service_name

_repository_duration: metrics.Histogram | None = None


def setup_otel(*, instrument_django: bool = True) -> None:
    """Initialize OTEL MeterProvider. Call once at process startup."""
    global _repository_duration  # noqa: PLW0603
    logger.info("Initializing OTEL")

    endpoint = os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"]

    resource = Resource(attributes={SERVICE_NAME: service_name})
    exporter = OTLPMetricExporter(endpoint=endpoint, insecure=True)
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60_000)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    logger.info("OTEL initialized")

    _repository_duration = get_meter("repository").create_histogram(
        f"{METRIC_PREFIX}.repository.call.duration",
        unit="s",
        description="Duration of external repository/API calls",
    )

    if instrument_django:
        logger.info("Instrumenting Django")
        DjangoInstrumentor().instrument()
        logger.info("Django instrumentation complete")


def get_meter(name: str) -> metrics.Meter:
    return metrics.get_meter_provider().get_meter(name)


@contextlib.contextmanager
def timed_repository_call(repository_name: str) -> Generator[None]:
    """Context manager to record external repository call duration."""
    start = time.perf_counter()
    try:
        yield
    finally:
        if _repository_duration is not None:
            _repository_duration.record(
                time.perf_counter() - start, {"repository": repository_name}
            )
