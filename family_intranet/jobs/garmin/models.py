import logging
from datetime import date, datetime
from typing import Any

from sqlalchemy import JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from family_intranet.jobs.garmin.db import Base

log = logging.getLogger(__name__)


class HeartRateDailyStats(Base):
    __tablename__ = "heart_rate_daily"

    measure_date: Mapped[date] = mapped_column(primary_key=True)
    resting_heart_rate: Mapped[int | None]
    min_heart_rate: Mapped[int | None]
    max_heart_rate: Mapped[int | None]
    last_seven_days_avg_resting_heart_rate: Mapped[int | None]


class HeartRate(Base):
    __tablename__ = "heart_rate"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    heart_rate: Mapped[int] = mapped_column(nullable=True)


class Steps(Base):
    __tablename__ = "steps"

    tstamp_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    tstamp_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    steps: Mapped[int]
    pushes: Mapped[int]
    primaryActivityLevel: Mapped[str]
    activityLevelConstant: Mapped[bool]


class StepsDaily(Base):
    __tablename__ = "steps_daily"

    calendar_date: Mapped[date] = mapped_column(primary_key=True)
    total_steps: Mapped[int | None]
    total_distance: Mapped[int | None]
    step_goal: Mapped[int | None]


class Floors(Base):
    __tablename__ = "floors"

    tstamp_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    tstamp_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    floorsAscended: Mapped[int]
    floorsDescended: Mapped[int]


class StressDaily(Base):
    __tablename__ = "stress_daily"

    calendar_date: Mapped[date] = mapped_column(primary_key=True)
    max_stress_level: Mapped[int | None]
    avg_stress_level: Mapped[int | None]
    stress_chart_value_offset: Mapped[int | None]
    stress_chart_y_axis_origin: Mapped[int | None]


class Stress(Base):
    __tablename__ = "stress"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    stress_level: Mapped[int]


class BodyBatteryDaily(Base):
    __tablename__ = "body_battery_daily"

    calendar_date: Mapped[date] = mapped_column(primary_key=True)
    charged: Mapped[int | None]
    drained: Mapped[int | None]
    dynamic_feedback_event: Mapped[dict[str, Any]] = mapped_column(type_=JSON)
    end_of_day_dynamic_feedback_event: Mapped[dict[str, Any]] = mapped_column(
        type_=JSON
    )


class BodyBattery(Base):
    __tablename__ = "body_battery"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    body_battery_status: Mapped[str | None]
    body_battery_level: Mapped[int | None]
    body_battery_version: Mapped[float | None]


class BodyBatteryActivityEvent(Base):
    __tablename__ = "body_battery_activity_event"

    tstamp_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    event_type: Mapped[str]
    duration_seconds: Mapped[int]
    body_battery_impact: Mapped[int]
    feedback_type: Mapped[str]
    short_feedback: Mapped[str]


class SleepDaily(Base):
    __tablename__ = "sleep_daily"

    calendar_date: Mapped[date] = mapped_column(primary_key=True)
    sleep_time_seconds: Mapped[int | None]
    nap_time_seconds: Mapped[int | None]
    sleep_start_tstamp: Mapped[datetime | None]
    sleep_end_tstamp: Mapped[datetime | None]
    unmeasurable_sleep_seconds: Mapped[int | None]
    deep_sleep_seconds: Mapped[int | None]
    light_sleep_seconds: Mapped[int | None]
    rem_sleep_seconds: Mapped[int | None]
    awake_sleep_seconds: Mapped[int | None]
    average_sp_o_2_value: Mapped[float | None]
    lowest_sp_o_2_value: Mapped[float | None]
    highest_sp_o_2_value: Mapped[float | None]
    average_sp_o_2_hrsleep: Mapped[float | None]
    average_respiration_value: Mapped[float | None]
    lowest_respiration_value: Mapped[float | None]
    highest_respiration_value: Mapped[float | None]
    awake_count: Mapped[int | None]
    avg_sleep_stress: Mapped[float | None]
    sleep_score_feedback: Mapped[str | None]
    sleep_score_insight: Mapped[str | None]
    sleep_score_personalized_insight: Mapped[str | None]
    restless_moments_count: Mapped[int | None]
    avg_overnight_hrv: Mapped[float | None]
    hrv_status: Mapped[str | None]
    body_battery_change: Mapped[int | None]
    resting_heart_rate: Mapped[int | None]
    sleep_scores: Mapped[dict[str, Any]] = mapped_column(type_=JSON)


class SleepMovement(Base):
    __tablename__ = "sleep_movement"

    tstamp_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    tstamp_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    activity_level: Mapped[float]


class SleepLevels(Base):
    __tablename__ = "sleep_levels"

    tstamp_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    tstamp_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    activity_level: Mapped[int]


class SleepRestlessMoments(Base):
    __tablename__ = "sleep_restless_moments"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    value: Mapped[int]


class SleepSPO2Data(Base):
    __tablename__ = "sleep_spo2_data"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    epoch_duration: Mapped[int | None]
    spo2_value: Mapped[int | None]
    reading_confidence: Mapped[int | None]


class SleepRespirationData(Base):
    __tablename__ = "sleep_respiration_data"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    respiration_value: Mapped[int]


class SleepHeartRate(Base):
    __tablename__ = "sleep_heart_rate"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    heart_rate: Mapped[int | None]


class SleepStress(Base):
    __tablename__ = "sleep_stress"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    stress_level: Mapped[int]


class SleepBodyBattery(Base):
    __tablename__ = "sleep_body_battery"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    body_battery_level: Mapped[int]


class SleepHRVData(Base):
    __tablename__ = "sleep_hrv_data"

    tstamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    hrv_value: Mapped[int]


class GarminLoadRun(Base):
    __tablename__ = "garmin_load_run"

    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    data_from_date: Mapped[date]
    data_to_date: Mapped[date]
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    success: Mapped[bool] = mapped_column(default=False)
    error_message: Mapped[str | None] = mapped_column(default=None)
