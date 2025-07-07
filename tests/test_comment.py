from loguru import logger

from app.models.models import Comment


def test_add_comment(setup_database, database_session, test_client, user_auth_header):
    scrap_id = 2
    content = "test comment"

    request = {
        'scrap_id': scrap_id,
        'comment': content
    }

    response = test_client.post(
        url="/comment",
        headers=user_auth_header,
        json=request
    )

    logger.debug("response : {}", response.json())

    assert response.status_code == 200

    comment = database_session.query(Comment).order_by(Comment.id.desc()).limit(1).first()

    assert comment
    assert scrap_id == comment.scrap_id
    assert content == comment.content


def test_get_comments_success(setup_database, database_session, test_client, user_auth_header):
    request = {
        'page': 1,
        'scrap_id': 1
    }

    response = test_client.get(
        url="/comment",
        params=request,
        headers=user_auth_header
    )

    assert 200 == response.status_code
    data = response.json()
    logger.debug("response : {}", data)

    assert 0 < data['data']['total_count']
    assert 0 < len(data['data']['content'])
