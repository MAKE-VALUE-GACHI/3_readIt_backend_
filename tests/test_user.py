from loguru import logger

from app.models.models import User


def test_get_user(setup_database, test_client, user_auth_header):
    response = test_client.get(url="/user", headers=user_auth_header)

    logger.debug("response : {}", response.json())

    assert response.status_code == 200


def test_update_user_success(setup_database, database_session, test_client, user_auth_header):
    user_id = 1
    name = "updated name"

    request = {
        'name': name
    }
    response = test_client.put(
        url=f"/user",
        json=request,
        headers=user_auth_header
    )

    assert 200 == response.status_code

    logger.debug("response : {}", response.json())

    user = database_session.query(User).filter(User.id == user_id).first()
    assert name == user.name
