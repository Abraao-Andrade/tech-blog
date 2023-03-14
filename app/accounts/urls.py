from django.urls import re_path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginAPIView,
    ForgotPasswordAPIView,
    ResetPasswordWithToken,
    ChangePasswordUserApiView,
    AccountAPIView,
    AccountCreateAPIView,
    AgreedAPIView,
    AccountMeRetrieveAPIView,
)

app_name = "accounts"

urlpatterns = [
    re_path(
        r"^(?P<version>(v1))/accounts/signin$",
        LoginAPIView.as_view(),
        name="signin",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/forgot$",
        ForgotPasswordAPIView.as_view(),
        name="forgot",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/refresh-token$",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/(?P<pk>\d+)$",
        AccountAPIView.as_view(),
        name="subscriber-detail",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/create",
        AccountCreateAPIView.as_view(),
        name="accounts-create",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/me?$",
        AccountMeRetrieveAPIView.as_view(),
        name="user-detail",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/agreed$",
        AgreedAPIView.as_view(),
        name="agreed",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/change-password$",
        ChangePasswordUserApiView.as_view(),
        name="change_forgot",
    ),
    re_path(
        r"^(?P<version>(v1))/accounts/reset-password",
        ResetPasswordWithToken.as_view(),
        name="reset_password",
    ),
]
