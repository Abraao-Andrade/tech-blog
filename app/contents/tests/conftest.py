import pytest
from django.utils import timezone

from app.contents.models import (
    Category,
    Article,
    Video,
)


@pytest.fixture
def category_1(db):
    return Category.objects.create(
        name="category test 1",
        description="desc test 1",
    )


@pytest.fixture
def category_inative(db):
    return Category.objects.create(
        name="category test inative",
        description="desc test inative",
        is_active=False,
    )


@pytest.fixture
def article_future(db, author, category):
    article_future = Article.objects.create(
        title="article test future",
        subtitle="subtitle test future",
        text="text test future",
        author=author,
        show_in_start=False,
        published_at=timezone.now() + timezone.timedelta(days=1),
    )
    article_future.categories.add(category)
    return article_future


@pytest.fixture
def video(db):
    return Video.objects.create(
        url="https://www.youtube.com/",
        title="title test",
        description="desc test",
        published_at=timezone.now(),
    )


@pytest.fixture
def video_future(db):
    return Video.objects.create(
        url="https://www.youtube.com/",
        title="title test future",
        description="desc test future",
        published_at=timezone.now() + timezone.timedelta(days=1),
    )
