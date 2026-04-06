import logging
import time
import traceback
from datetime import UTC, date, datetime

from dateutil.relativedelta import relativedelta
from django.tasks import task
from sqlalchemy.orm import Session

from family_intranet.jobs.garmin import client, db, loaders, models
from family_intranet.otel import METRIC_PREFIX, get_meter

logger = logging.getLogger(__name__)

_meter = get_meter("garmin")
_job_duration = _meter.create_histogram(
    f"{METRIC_PREFIX}.garmin.job.duration",
    unit="s",
    description="Total Garmin load job duration",
)
_job_runs = _meter.create_counter(
    f"{METRIC_PREFIX}.garmin.job.runs",
    description="Number of Garmin load job executions",
)
_loader_rows = _meter.create_counter(
    f"{METRIC_PREFIX}.garmin.loader.rows_saved",
    unit="rows",
    description="Rows saved per Garmin loader call",
)


def _get_last_successful_run_date() -> date:
    """Get the end date of the last successful run from the DB.

    Falls back to determining from existing data if no run record exists.
    """
    engine = db.get_engine()
    with Session(engine) as session:
        last_run = (
            session.query(models.GarminLoadRun)
            .filter(models.GarminLoadRun.success == True)  # noqa: E712
            .order_by(models.GarminLoadRun.finished_at.desc())
            .first()
        )
        logger.info(f"Last successful run: {last_run}")
        if last_run:
            return last_run.data_to_date

    return date(2026, 2, 24)


@task
def run_garmin_load() -> None:
    """Hourly scheduled job: loads all Garmin data since last successful run."""
    started_at = datetime.now(tz=UTC)

    # Ensure tables exist
    db.Base.metadata.create_all(db.get_engine())

    start_date = _get_last_successful_run_date()
    logger.info("Starting Garmin load for %s.", start_date)
    end_date = date.today()

    logger.info("Garmin load: %s to %s", start_date, end_date)

    run_record = models.GarminLoadRun(
        started_at=started_at,
        data_from_date=start_date,
        data_to_date=end_date,
    )

    job_start = time.perf_counter()
    try:
        garmin_client = client.get_garmin_client()
        for day_offset in range((end_date - start_date).days + 1):
            measure_date = start_date + relativedelta(days=day_offset)
            _loader_rows.add(
                loaders.get_heartrate_data(
                    measure_date=measure_date, garmin_client=garmin_client
                ),
                {"loader": "heartrate"},
            )
            _loader_rows.add(
                loaders.get_steps_data(
                    measure_date=measure_date, garmin_client=garmin_client
                ),
                {"loader": "steps"},
            )
            _loader_rows.add(
                loaders.get_daily_steps_data(
                    measure_date=measure_date, garmin_client=garmin_client
                ),
                {"loader": "daily_steps"},
            )
            _loader_rows.add(
                loaders.get_floors_data(
                    measure_date=measure_date, garmin_client=garmin_client
                ),
                {"loader": "floors"},
            )
            _loader_rows.add(
                loaders.get_stress_data(
                    measure_date=measure_date, garmin_client=garmin_client
                ),
                {"loader": "stress"},
            )
            _loader_rows.add(
                loaders.get_body_battery_data(
                    measure_date=measure_date, garmin_client=garmin_client
                ),
                {"loader": "body_battery"},
            )
            _loader_rows.add(
                loaders.get_sleep_data(
                    measure_date=measure_date, garmin_client=garmin_client
                ),
                {"loader": "sleep"},
            )

        run_record.success = True
        run_record.finished_at = datetime.now(tz=UTC)
        db.save_objects((run_record,), upsert=False)
        _job_runs.add(1, {"status": "success"})
        _job_duration.record(time.perf_counter() - job_start)
        logger.info("Garmin load completed successfully.")
    except Exception:
        run_record.success = False
        run_record.finished_at = datetime.now(tz=UTC)
        run_record.error_message = traceback.format_exc()
        logger.exception("Garmin load failed.")
        db.save_objects((run_record,), upsert=False)
        _job_runs.add(1, {"status": "failed"})
        _job_duration.record(time.perf_counter() - job_start)
        raise
