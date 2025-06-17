import pytest
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.config import settings
from app.db.session import engine_url


@pytest.fixture(scope="function")
def setup_database():
    if not database_exists(engine_url):
        create_database(engine_url)

    alembic_config = Config('alembic.ini')

    try:
        alembic_config.set_main_option('sqlalchemy.url', str(engine_url))
        alembic_config.set_main_option('script_location', 'migrations/')
        upgrade(alembic_config, "head")

        yield

    except Exception as ex:
        raise ex

    finally:
        if settings.DATABASE_HOST == "localhost":
            drop_database(engine_url)
