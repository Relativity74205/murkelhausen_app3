import logging
from collections.abc import Iterable

from django.conf import settings
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session

log = logging.getLogger(__name__)


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


def get_engine():
    url = URL.create(
        drivername="postgresql+psycopg",
        username=settings.GARMIN_DB_USER,
        password=settings.GARMIN_DB_PASSWORD,
        host=settings.GARMIN_DB_HOST,
        port=settings.GARMIN_DB_PORT,
        database=settings.GARMIN_DB_NAME,
    )
    return create_engine(
        url,
        echo=False,
        connect_args={"options": f"-csearch_path={settings.GARMIN_DB_SCHEMA}"},
    )


def save_objects(objects: Iterable[Base], *, upsert: bool = True):
    engine = get_engine()
    with Session(engine) as session:
        if upsert:
            for o in objects:
                session.merge(o)
        else:
            session.add_all(objects)
        session.commit()
