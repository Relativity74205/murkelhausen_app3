import logging
from datetime import UTC, date, datetime

import pytz
from garminconnect import Garmin

from family_intranet.jobs.garmin import models
from family_intranet.jobs.garmin.db import save_objects

logger = logging.getLogger(__name__)


def _unaware_utc_string_to_europe_berlin_datetime(s: str) -> datetime:
    return (
        datetime.fromisoformat(s)
        .replace(tzinfo=UTC)
        .astimezone(pytz.timezone("Europe/Berlin"))
    )


def _unix_timestamp_millis_to_europe_berlin_datetime(t: int | None) -> datetime | None:
    if t is None:
        return None
    return datetime.fromtimestamp(t / 1000, tz=pytz.UTC).astimezone(
        pytz.timezone("Europe/Berlin")
    )


def get_heartrate_data(*, measure_date: date, garmin_client: Garmin) -> int:
    """Returns the amount of heart rate data points saved."""
    logger.info("Getting heart rate data for %s.", measure_date)
    data = garmin_client.get_heart_rates(measure_date.isoformat())
    heart_rates_daily = models.HeartRateDailyStats(
        measure_date=measure_date,
        resting_heart_rate=data["restingHeartRate"],
        min_heart_rate=data["minHeartRate"],
        max_heart_rate=data["maxHeartRate"],
        last_seven_days_avg_resting_heart_rate=data["lastSevenDaysAvgRestingHeartRate"],
    )
    if data["heartRateValues"] is not None:
        heart_rates = tuple(
            models.HeartRate(
                tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(entry[0]),
                heart_rate=entry[1],
            )
            for entry in data["heartRateValues"]
        )
    else:
        heart_rates = ()

    logger.info("Got %d heart rate data points. Saving.", len(heart_rates))
    save_objects((heart_rates_daily,), upsert=True)
    save_objects(heart_rates, upsert=True)
    return len(heart_rates)


def get_steps_data(*, measure_date: date, garmin_client: Garmin) -> int:
    """Returns the amount of steps data points saved."""
    logger.info("Getting steps data for %s.", measure_date)
    data = garmin_client.get_steps_data(measure_date.isoformat())
    steps = tuple(
        models.Steps(
            tstamp_start=_unaware_utc_string_to_europe_berlin_datetime(
                entry["startGMT"]
            ),
            tstamp_end=_unaware_utc_string_to_europe_berlin_datetime(entry["endGMT"]),
            steps=entry["steps"],
            pushes=entry["pushes"],
            primaryActivityLevel=entry["primaryActivityLevel"],
            activityLevelConstant=entry["activityLevelConstant"],
        )
        for entry in data
    )
    logger.info("Got %d steps data points. Saving.", len(steps))
    save_objects(steps, upsert=True)
    return len(steps)


def get_daily_steps_data(*, measure_date: date, garmin_client: Garmin) -> int:
    """Returns the amount of daily steps data points saved."""
    logger.info("Getting daily steps data for %s.", measure_date)
    data = garmin_client.get_daily_steps(start=measure_date.isoformat(), end=measure_date.isoformat())
    steps = tuple(
        models.StepsDaily(
            calendar_date=date.fromisoformat(entry["calendarDate"]),
            total_steps=entry["totalSteps"],
            total_distance=entry["totalDistance"],
            step_goal=entry["stepGoal"],
        )
        for entry in data
    )
    logger.info("Got %d daily steps data points. Saving.", len(steps))
    save_objects(steps, upsert=True)
    return len(steps)


def get_floors_data(*, measure_date: date, garmin_client: Garmin) -> int:
    """Returns the amount of floors data points saved."""
    logger.info("Getting floors data for %s.", measure_date)
    data = garmin_client.get_floors(measure_date.isoformat())
    floors = tuple(
        models.Floors(
            tstamp_start=_unaware_utc_string_to_europe_berlin_datetime(entry[0]),
            tstamp_end=_unaware_utc_string_to_europe_berlin_datetime(entry[1]),
            floorsAscended=entry[2],
            floorsDescended=entry[3],
        )
        for entry in data.get("floorValuesArray", ())
    )
    logger.info("Got %d floors data points. Saving.", len(floors))
    save_objects(floors, upsert=True)
    return len(floors)


def get_stress_data(*, measure_date: date, garmin_client: Garmin) -> int:
    """Returns the amount of stress data points saved."""
    logger.info("Getting stress data for %s.", measure_date)
    data = garmin_client.get_stress_data(measure_date.isoformat())
    stress = tuple(
        models.Stress(
            tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(entry[0]),
            stress_level=entry[1],
        )
        for entry in data["stressValuesArray"]
    )
    stress_daily = models.StressDaily(
        calendar_date=date.fromisoformat(data["calendarDate"]),
        max_stress_level=data["maxStressLevel"],
        avg_stress_level=data["avgStressLevel"],
        stress_chart_value_offset=data["stressChartValueOffset"],
        stress_chart_y_axis_origin=data["stressChartYAxisOrigin"],
    )
    logger.info("Got %d stress data points. Saving.", len(stress))
    save_objects(stress, upsert=True)
    save_objects((stress_daily,), upsert=True)
    return len(stress)


def get_body_battery_data(*, measure_date: date, garmin_client: Garmin) -> int:
    """Returns the amount of body battery data points saved."""
    logger.info("Getting body battery data for %s.", measure_date)
    data_stress = garmin_client.get_stress_data(measure_date.isoformat())
    body_battery = tuple(
        models.BodyBattery(
            tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(entry[0]),
            body_battery_status=entry[1],
            body_battery_level=entry[2],
            body_battery_version=entry[3],
        )
        for entry in data_stress.get("bodyBatteryValuesArray", ())
    )
    logger.info("Got %d body battery data points. Saving.", len(body_battery))
    save_objects(body_battery, upsert=True)

    data_body = garmin_client.get_body_battery(measure_date.isoformat())
    body_battery_daily = models.BodyBatteryDaily(
        calendar_date=date.fromisoformat(data_body[0]["date"]),
        charged=data_body[0]["charged"],
        drained=data_body[0]["drained"],
        dynamic_feedback_event=data_body[0].get("bodyBatteryDynamicFeedbackEvent", {}),
        end_of_day_dynamic_feedback_event=data_body[0].get(
            "endOfDayBodyBatteryDynamicFeedbackEvent", {}
        ),
    )
    save_objects((body_battery_daily,), upsert=True)

    body_battery_activity_events = tuple(
        models.BodyBatteryActivityEvent(
            tstamp_start=_unaware_utc_string_to_europe_berlin_datetime(
                entry["eventStartTimeGmt"]
            ),
            event_type=entry["eventType"],
            duration_seconds=int(entry["durationInMilliseconds"] / 1000),
            body_battery_impact=entry["bodyBatteryImpact"],
            feedback_type=entry["feedbackType"],
            short_feedback=entry["shortFeedback"],
        )
        for entry in data_body[0].get("bodyBatteryActivityEvent", ())
    )
    save_objects(body_battery_activity_events, upsert=True)
    return len(body_battery)


def _get_sleep_data_daily(data_sleep: dict, /) -> None:
    daily_sleep = data_sleep["dailySleepDTO"]
    if daily_sleep["calendarDate"] is None:
        logger.info("No sleep data for this day (yet). Skipping.")
        return

    sleep_daily = models.SleepDaily(
        calendar_date=date.fromisoformat(daily_sleep["calendarDate"]),
        sleep_time_seconds=daily_sleep.get("sleepTimeSeconds"),
        nap_time_seconds=daily_sleep.get("napTimeSeconds"),
        sleep_start_tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
            daily_sleep.get("sleepStartTimestampGMT")
        ),
        sleep_end_tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
            daily_sleep.get("sleepEndTimestampGMT")
        ),
        unmeasurable_sleep_seconds=daily_sleep.get("unmeasurableSleepSeconds"),
        deep_sleep_seconds=daily_sleep.get("deepSleepSeconds"),
        light_sleep_seconds=daily_sleep.get("lightSleepSeconds"),
        rem_sleep_seconds=daily_sleep.get("remSleepSeconds"),
        awake_sleep_seconds=daily_sleep.get("awakeSleepSeconds"),
        average_sp_o_2_value=daily_sleep.get("averageSpO2Value"),
        lowest_sp_o_2_value=daily_sleep.get("lowestSpO2Value"),
        highest_sp_o_2_value=daily_sleep.get("highestSpO2Value"),
        average_sp_o_2_hrsleep=daily_sleep.get("averageSpO2HRSleep"),
        average_respiration_value=daily_sleep.get("averageRespirationValue"),
        lowest_respiration_value=daily_sleep.get("lowestRespirationValue"),
        highest_respiration_value=daily_sleep.get("highestRespirationValue"),
        awake_count=daily_sleep.get("awakeCount"),
        avg_sleep_stress=daily_sleep.get("avgSleepStress"),
        sleep_score_feedback=daily_sleep.get("sleepScoreFeedback"),
        sleep_score_insight=daily_sleep.get("sleepScoreInsight"),
        sleep_score_personalized_insight=daily_sleep.get(
            "sleepScorePersonalizedInsight"
        ),
        restless_moments_count=data_sleep.get("restlessMomentsCount"),
        avg_overnight_hrv=data_sleep.get("avgOvernightHrv"),
        hrv_status=data_sleep.get("hrvStatus"),
        body_battery_change=data_sleep.get("bodyBatteryChange"),
        resting_heart_rate=data_sleep.get("restingHeartRate"),
        sleep_scores=daily_sleep.get("sleepScores"),
    )
    save_objects((sleep_daily,), upsert=True)
    logger.info("Saved sleep daily data.")


def get_sleep_data(*, measure_date: date, garmin_client: Garmin) -> int:
    """Returns the amount of sleep data points saved."""
    logger.info("Getting sleep data for %s.", measure_date)

    data_sleep = garmin_client.get_sleep_data(measure_date.isoformat())
    _get_sleep_data_daily(data_sleep)

    total = 0

    if data_sleep.get("sleepMovement") is not None:
        sleep_movements = tuple(
            models.SleepMovement(
                tstamp_start=_unaware_utc_string_to_europe_berlin_datetime(
                    entry["startGMT"]
                ),
                tstamp_end=_unaware_utc_string_to_europe_berlin_datetime(
                    entry["endGMT"]
                ),
                activity_level=entry["activityLevel"],
            )
            for entry in data_sleep["sleepMovement"]
        )
        save_objects(sleep_movements, upsert=True)
        total += len(sleep_movements)
        logger.info("Saved sleep movements data (%d rows).", len(sleep_movements))

    if data_sleep.get("sleepLevels") is not None:
        sleep_levels = tuple(
            models.SleepLevels(
                tstamp_start=_unaware_utc_string_to_europe_berlin_datetime(
                    entry["startGMT"]
                ),
                tstamp_end=_unaware_utc_string_to_europe_berlin_datetime(
                    entry["endGMT"]
                ),
                activity_level=int(entry["activityLevel"]),
            )
            for entry in data_sleep["sleepLevels"]
        )
        save_objects(sleep_levels, upsert=True)
        total += len(sleep_levels)
        logger.info("Saved sleep levels data (%d rows).", len(sleep_levels))

    if data_sleep.get("sleepRestlessMoments") is not None:
        sleep_restless_moments = tuple(
            models.SleepRestlessMoments(
                tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
                    entry["startGMT"]
                ),
                value=int(entry["value"]),
            )
            for entry in data_sleep["sleepRestlessMoments"]
        )
        save_objects(sleep_restless_moments, upsert=True)
        total += len(sleep_restless_moments)
        logger.info(
            "Saved sleep restless moments data (%d rows).", len(sleep_restless_moments)
        )

    if data_sleep.get("wellnessEpochSPO2DataDTOList") is not None:
        sleep_spo2_data = tuple(
            models.SleepSPO2Data(
                tstamp=_unaware_utc_string_to_europe_berlin_datetime(
                    entry["epochTimestamp"]
                ),
                epoch_duration=entry["epochDuration"],
                spo2_value=entry["spo2Reading"],
                reading_confidence=entry["readingConfidence"],
            )
            for entry in data_sleep["wellnessEpochSPO2DataDTOList"]
        )
        save_objects(sleep_spo2_data, upsert=True)
        total += len(sleep_spo2_data)
        logger.info("Saved sleep spo2 data (%d rows).", len(sleep_spo2_data))

    if data_sleep.get("wellnessEpochRespirationDataDTOList") is not None:
        sleep_respiration_data = tuple(
            models.SleepRespirationData(
                tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
                    entry["startTimeGMT"]
                ),
                respiration_value=int(entry["respirationValue"]),
            )
            for entry in data_sleep["wellnessEpochRespirationDataDTOList"]
        )
        save_objects(sleep_respiration_data, upsert=True)
        total += len(sleep_respiration_data)
        logger.info(
            "Saved sleep respiration data (%d rows).", len(sleep_respiration_data)
        )

    if data_sleep.get("sleepHeartRate") is not None:
        sleep_heart_rates = tuple(
            models.SleepHeartRate(
                tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
                    entry["startGMT"]
                ),
                heart_rate=entry["value"],
            )
            for entry in data_sleep["sleepHeartRate"]
        )
        save_objects(sleep_heart_rates, upsert=True)
        total += len(sleep_heart_rates)
        logger.info("Saved sleep heart rate data (%d rows).", len(sleep_heart_rates))

    if data_sleep.get("sleepStress") is not None:
        sleep_stress_data = tuple(
            models.SleepStress(
                tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
                    entry["startGMT"]
                ),
                stress_level=int(entry["value"]),
            )
            for entry in data_sleep["sleepStress"]
        )
        save_objects(sleep_stress_data, upsert=True)
        total += len(sleep_stress_data)
        logger.info("Saved sleep stress data (%d rows).", len(sleep_stress_data))

    if data_sleep.get("sleepBodyBattery") is not None:
        sleep_body_battery_data = tuple(
            models.SleepBodyBattery(
                tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
                    entry["startGMT"]
                ),
                body_battery_level=int(entry["value"]),
            )
            for entry in data_sleep["sleepBodyBattery"]
        )
        save_objects(sleep_body_battery_data, upsert=True)
        total += len(sleep_body_battery_data)
        logger.info(
            "Saved sleep body battery data (%d rows).", len(sleep_body_battery_data)
        )

    if data_sleep.get("hrvData") is not None:
        sleep_hrv_data = tuple(
            models.SleepHRVData(
                tstamp=_unix_timestamp_millis_to_europe_berlin_datetime(
                    entry["startGMT"]
                ),
                hrv_value=int(entry["value"]),
            )
            for entry in data_sleep["hrvData"]
        )
        save_objects(sleep_hrv_data, upsert=True)
        total += len(sleep_hrv_data)
        logger.info("Saved sleep hrv data (%d rows).", len(sleep_hrv_data))

    return total
