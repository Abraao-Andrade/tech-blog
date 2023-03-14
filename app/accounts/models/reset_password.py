import hashlib

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.db import models

from rest_framework.request import Request

from model_utils.fields import AutoCreatedField
from app.common import utils


def expires_in() -> timezone:
    days = getattr(settings, "TOKEN_RESET_EXPIRED", 1)
    return timezone.now() + timezone.timedelta(days=days)


class ResetPassword(models.Model):
    token = models.CharField(max_length=500)
    sending_attempts = models.PositiveIntegerField(
        default=0, verbose_name="Quantidade de Solicitações"
    )
    ip = models.GenericIPAddressField(blank=True, null=True)
    agent = models.CharField(max_length=500, blank=True, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = AutoCreatedField(db_index=True, verbose_name=_("Criado em"))
    updated_at = AutoCreatedField(db_index=True, verbose_name=_("Atualizado em"))
    expires_in = AutoCreatedField(
        db_index=True, verbose_name=_("Token expira em"), default=expires_in
    )

    class Meta:
        verbose_name = "Solicitou Troca de Senha"
        verbose_name_plural = "Solicitou Troca de Senha"
        db_table = "accounts_resetpassword"

    def __str__(self) -> str:
        return getattr(self.user, "email")

    @property
    def is_invalid(self) -> bool:
        return timezone.now() > self.expires_in

    def get_token(self, user: settings.AUTH_USER_MODEL) -> str:
        return utils.jwt_encode(
            {
                "token": hashlib.md5(
                    default_token_generator.make_token(user).encode()
                ).hexdigest()
            }
        )

    def generation_token(
        self, user: settings.AUTH_USER_MODEL, request: Request
    ) -> object:
        token = self.get_token(user)

        reset_password_token = ResetPassword.objects.filter(user=user).first()

        if reset_password_token and reset_password_token.is_invalid:
            reset_password_token.delete()
            reset_password_token = ResetPassword.objects.create(
                token=token, user=user, **utils.get_ip_and_agent(request)
            )
        elif not reset_password_token:
            reset_password_token = ResetPassword.objects.create(
                token=token, user=user, **utils.get_ip_and_agent(request)
            )
        return reset_password_token

    def create_history(self) -> None:
        data = self.__dict__.copy()
        data.pop("_state")
        data.pop("id")
        data.update({"change_in": timezone.now()})
        HistoryResetPassword(**data).save()

    def incr_attempts(self) -> None:
        ResetPassword.objects.filter(pk=self.pk).update(
            sending_attempts=models.F("sending_attempts") + 1, updated_at=timezone.now()
        )

    @property
    def name(self) -> str:
        return getattr(self.user, "name")

    @property
    def email(self) -> str:
        return getattr(self.user, "email")

    @property
    def link(self) -> str:
        return f"{settings.DOMAIN}/reset-password?token={self.token}"


class HistoryResetPassword(models.Model):
    token = models.CharField(max_length=500)
    ip = models.GenericIPAddressField(blank=True, null=True)
    agent = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    sending_attempts = models.PositiveIntegerField(default=0)
    expires_in = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Expira em"), default=expires_in
    )
    change_in = models.DateTimeField(verbose_name="Criou uma nova senha às:")
    updated_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Atualizado em")
    )
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Histórico de Troca de Senha"
        verbose_name_plural = "Histórico de Troca de Senhas"
        db_table = "accounts_reset_history_password"

    def __str__(self) -> str:
        return getattr(self.user, "email")

    @property
    def name(self) -> str:
        return getattr(self.user, "name")

    @property
    def email(self) -> str:
        return getattr(self.user, "email")
