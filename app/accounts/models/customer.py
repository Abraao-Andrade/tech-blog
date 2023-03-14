from ..models import User
from ..managers import UserManager

from app.common.choices import TYPE_USER


class Customer(User):
    objects = UserManager(type=TYPE_USER.customer)

    class Meta:
        proxy = True
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = TYPE_USER.customer
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)
