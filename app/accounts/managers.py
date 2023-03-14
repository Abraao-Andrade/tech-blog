from django.contrib.auth.models import BaseUserManager
from django.http import HttpRequest

from app.common.choices import TYPE_USER
from app.common import utils


class UserManager(BaseUserManager):
    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop("type", TYPE_USER.customer)
        super().__init__(*args, **kwargs)

    def add_ip_agent(self, user, request: HttpRequest) -> None:
        if request:
            data = utils.get_ip_and_agent(request)
            user.ip = data.get("ip")
            user.agent = data.get("agent")

    def create_user(self, email, password=None, **kwargs):
        email = utils.normalize_email(email)
        request = kwargs.pop("request", None)
        user = self.model(email=email, **kwargs)
        self.add_ip_agent(user, request)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.type = TYPE_USER.admin
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        if self.type:
            kwargs.update({"type": self.type})
        user = super().create(**kwargs)
        user.set_password(kwargs.get("password"))
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(type__in=self.type.split(", "))
            .filter(deleted_at__isnull=True)
        )
