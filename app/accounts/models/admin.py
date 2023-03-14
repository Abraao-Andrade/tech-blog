from ..models import User
from ..managers import UserManager

from app.common.choices import TYPE_USER


class Admin(User):
    objects = UserManager(type=TYPE_USER.admin)

    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Administradores"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = TYPE_USER.admin
            self.is_superuser = True
            self.is_staff = True
        super().save(*args, **kwargs)
