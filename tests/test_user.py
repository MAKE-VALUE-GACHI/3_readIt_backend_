from loguru import logger

from app.models.models import User, Scrap


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
        url="/user",
        json=request,
        headers=user_auth_header
    )

    assert 200 == response.status_code

    logger.debug("response : {}", response.json())

    user = database_session.query(User).filter(User.id == user_id).first()
    assert name == user.name


def test_get_user_scraps_success(setup_database, database_session, test_client, user_auth_header):
    request = {
        'page': 1,
        'category': "뉴스"
    }

    response = test_client.get(
        url="/user/scraps",
        params=request,
        headers=user_auth_header
    )

    assert 200 == response.status_code
    data = response.json()
    logger.debug("response : {}", data)

    assert 0 < data['data']['total_count']
    assert 0 < len(data['data']['content'])


def test_set_scrap_visibility_success(setup_database, database_session, test_client, user_auth_header):
    scrap_id = 2
    is_public = True

    request = {
        'scrap_id': scrap_id,
        'is_public': is_public
    }
    response = test_client.patch(
        url="/user/scrap/visibility",
        json=request,
        headers=user_auth_header
    )

    assert 200 == response.status_code

    logger.debug("response : {}", response.json())

    scrap = database_session.query(Scrap).filter(Scrap.id == scrap_id).first()

    assert is_public == scrap.is_public
