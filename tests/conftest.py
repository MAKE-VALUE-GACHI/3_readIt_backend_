import sys

import pytest
from alembic.command import upgrade
from alembic.config import Config
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.config import settings
from app.main import app
from app.security import jwt_provider

logger.remove()

logger.add(
    sys.stdout,
    format="[<blue>{time:YYYY-MM-DD HH:mm:ss}</blue>][<level>{level}</level>][{name}|{function}:{line}] -> {message}",
    colorize=True,
)


@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as api_client:
        yield api_client


@pytest.fixture(scope="function")
def setup_database():
    url = URL.create(
        drivername="mysql+mysqlconnector",
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        database=settings.DATABASE_NAME,
    ).render_as_string(hide_password=False)

    logger.debug("connect url : {}", url)

    if not database_exists(url):
        create_database(url)

    alembic_config = Config('alembic.ini')

    try:
        alembic_config.set_main_option('sqlalchemy.url', url.replace('%', '%%'))
        alembic_config.set_main_option('script_location', 'migrations/')
        upgrade(alembic_config, "head")

        yield

    except Exception as ex:
        logger.error(sys.exc_info())
        raise ex

    finally:
        if settings.DATABASE_HOST == "localhost":
            drop_database(url)


@pytest.fixture(scope="function")
def database_session(setup_database):
    engine = create_engine(
        url=f"mysql+mysqlconnector://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}",
        echo=True
    )
    connection = engine.connect()
    session = sessionmaker(bind=connection)()

    try:
        yield session  # 테스트 실행

    except (Exception,):
        session.rollback()
        session.close()
        raise

    finally:
        session.rollback()
        session.close()


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def user_auth_header():
    token = jwt_provider.create_access_token(user_id=1, additional_claims={'email': "test"})
    return {'Authorization': f"Bearer {token}"}
