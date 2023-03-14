from django.contrib.auth.hashers import make_password
from app.accounts.models import User


def test_user(db):
    User.objects.create_user(
        name="Username 1",
        email="test@test.com",
        password=make_password("abc123"),
        is_active=True,
        is_staff=False,
        is_superuser=False,
        phone="75999999999",
    )

    assert User.objects.count() == 1
