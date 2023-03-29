import json
from django.shortcuts import reverse
from rest_framework import status
from app.accounts.models import ResetPassword


def test_change_password_user_success(client, user, token):

    payload = json.dumps({"password": "abc1234", "password_old": "abc123"})

    response = client.put(
        reverse("accounts:change_forgot", kwargs={"version": "v1"}),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="JWT {}".format(token),
    )

    assert response.status_code == status.HTTP_200_OK

    response = client.post(
        reverse("accounts:signin", kwargs={"version": "v1"}),
        data=json.dumps({"email": "test@test.com", "password": "abc1234"}),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK


def test_change_password_user_fail(client, user, token):
    payload = json.dumps({"password": "abc1234", "password_old": "abc1234"})

    response = client.put(
        reverse("accounts:change_forgot", kwargs={"version": "v1"}),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="JWT {}".format(token),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_recovery_password(mocker, client, user):

    send_mail = mocker.patch(
        "app.accounts.tasks.email_recovery_password.delay", return_value=True
    )

    assert ResetPassword.objects.count() == 0

    payload = json.dumps({"email": user.email})
    response = client.post(
        reverse("accounts:forgot", kwargs={"version": "v1"}),
        content_type="application/json",
        data=payload,
    )

    assert ResetPassword.objects.count() == 1
    assert ResetPassword.objects.first().sending_attempts == 1
    assert send_mail.call_count == 1
    assert response.status_code == status.HTTP_200_OK
