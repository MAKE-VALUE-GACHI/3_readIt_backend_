from loguru import logger

from app.models.models import Scrap


def test_like_success(setup_database, database_session, test_client, user_auth_header):
    scrap_id = 1

    response = test_client.patch(url=f"/scrap/{scrap_id}/like", headers=user_auth_header)

    logger.debug("response : {}", response.json())

    assert response.status_code == 200

    scrap = database_session.query(Scrap).where(Scrap.id == scrap_id).first()

    assert 1 == scrap.like_count


def test_unlike_success(setup_database, database_session, test_client, user_auth_header):
    scrap_id = 2

    response = test_client.patch(url=f"/scrap/{scrap_id}/unlike", headers=user_auth_header)

    logger.debug("response : {}", response.json())

    assert response.status_code == 200

    scrap = database_session.query(Scrap).where(Scrap.id == scrap_id).first()

    assert 0 == scrap.like_count
