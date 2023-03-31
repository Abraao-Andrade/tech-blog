import pytest

from app.comments.models import Comment


@pytest.fixture
def comment(db, article):
    return Comment.objects.create(
        name="user test",
        email="test@test.com",
        text="test test",
        article=article,
    )
