import json
import pytest
from django.shortcuts import reverse
from app.accounts.models import User
from config.celery import app as celeryapp
from django.utils import timezone

from app.contents.models import (
    Category,
    Author,
    Article,
)


@pytest.fixture
def user(db):
    return User.objects.create_user(
        name="Username 1",
        email="test@test.com",
        password="abc123",
        is_active=True,
        is_staff=False,
        is_superuser=False,
        phone="75999999999",
    )


@pytest.fixture
def token(db, client, mocker, user):
    response = client.post(
        reverse("accounts:signin", kwargs={"version": "v1"}),
        data=json.dumps({"email": "test@test.com", "password": "abc123"}),
        content_type="application/json",
    )
    return response.json().get("token")


@pytest.fixture
def user1(db):
    return User.objects.create_user(
        name="Username 2",
        email="test1@test.com",
        password="abc123",
        is_active=True,
        is_staff=False,
        is_superuser=False,
        phone="75999999999",
    )


@pytest.fixture
def token1(db, client, mocker, user1):
    response = client.post(
        reverse("accounts:signin", kwargs={"version": "v1"}),
        data=json.dumps({"email": "test1@test.com", "password": "abc123"}),
        content_type="application/json",
    )
    return response.json().get("token")


@pytest.fixture(scope="module")
def celery_app():
    celeryapp.conf.update(task_always_eager=True)
    return celeryapp


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="category test",
        description="desc test",
    )


@pytest.fixture
def author(db):
    return Author.objects.create(
        name="category test",
        profession="profession test",
        description="desc test",
    )


@pytest.fixture
def article(db, author, category):
    article = Article.objects.create(
        title="article test",
        subtitle="subtitle test",
        text="text test",
        author=author,
        show_in_start=True,
        published_at=timezone.now(),
        banner="09123-1234",
    )
    article.categories.add(category)
    return article
