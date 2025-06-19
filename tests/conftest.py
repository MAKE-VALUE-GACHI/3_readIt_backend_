import sys

import pytest
from alembic.command import upgrade
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import URL
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.config import settings


@pytest.fixture(scope="function")
def test_client():
    from app.main import app

    with TestClient(app) as api_client:
        yield api_client


@pytest.fixture(scope="function")
def setup_database():
    url = URL.create(
        drivername="mysql+pymysql",
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        database=settings.DATABASE_NAME,
    )
    print(url.render_as_string(hide_password=False))

    if not database_exists(url):
        create_database(url)

    alembic_config = Config('alembic.ini')

    try:
        alembic_config.set_main_option('sqlalchemy.url', str(url))
        alembic_config.set_main_option('script_location', 'migrations/')
        upgrade(alembic_config, "head")

        yield

    except Exception as ex:
        print(sys.exc_info())
        raise ex

    finally:
        if settings.DATABASE_HOST == "localhost":
            drop_database(url)
