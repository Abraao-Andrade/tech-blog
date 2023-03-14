import json
import pytest
from django.shortcuts import reverse
from app.accounts.models import User
from config.celery import app as celeryapp


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
