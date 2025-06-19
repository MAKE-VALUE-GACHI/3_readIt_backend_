from loguru import logger


def test_get_user(setup_database, test_client):
    response = test_client.get("/user/1")

    logger.debug("response : {}", response.json())

    assert response.status_code == 200
