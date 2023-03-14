import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from app.common.models import TimeStampModel, SoftDeletionModel
from app.common.fields import ImageField
from app.common import choices
from app.accounts.managers import UserManager
from app.common.active_campaign import ActiveCampaign  # noqa


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel, SoftDeletionModel):
    name = models.CharField(
        max_length=255, verbose_name=_("Nome"), null=True, blank=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name=_("Sobrenome"), null=True, blank=True
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=_("Email"),
        unique=True,
        error_messages={"unique": "Usuário com e-mail já existente."},
    )
    phone = models.CharField(
        max_length=20, verbose_name=_("Telefone"), blank=True, null=True
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
        verbose_name=_("Acesso ao Dashboard?"),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
        verbose_name=_("Ativo?"),
    )
    photo = ImageField(
        upload_to=_("avatar-photo"), verbose_name=_("Foto"), help_text=_("Avatar")
    )
    document = models.CharField(
        max_length=40, verbose_name=_("Documento"), blank=True, null=True
    )
    birth_date = models.DateField(
        verbose_name=_("Data de nascimento"), blank=True, null=True
    )
    city = models.CharField(
        max_length=50, verbose_name=_("Cidade"), blank=True, null=True
    )
    state = models.CharField(
        max_length=2, verbose_name=_("Estado"), blank=True, null=True
    )
    address = models.CharField(
        max_length=100, verbose_name=_("Endereço"), blank=True, null=True
    )
    number = models.CharField(
        max_length=10, verbose_name=_("Número"), blank=True, null=True
    )
    district = models.CharField(
        max_length=50, verbose_name=_("Bairro"), blank=True, null=True
    )
    complement = models.CharField(
        max_length=250, verbose_name=_("Complemento"), blank=True, null=True
    )
    zipcode = models.CharField(
        max_length=50, verbose_name=_("CEP"), blank=True, null=True
    )
    agent = models.CharField(
        max_length=250, verbose_name=_("Dispositivo"), blank=True, null=True
    )
    ip = models.GenericIPAddressField(blank=True, null=True)
    hash_token = models.UUIDField(max_length=100, blank=True, null=True, editable=False)
    type = models.CharField(
        max_length=20, default="customer", choices=choices.TYPE_USER
    )
    objects = UserManager(type="admin, customer")

    agreed_at = models.DateTimeField(blank=True, null=True, editable=False)
    agreed_agent = models.CharField(
        max_length=250,
        verbose_name="Dispositivo",
        blank=True,
        null=True,
        editable=False,
    )
    agreed_ip = models.GenericIPAddressField(blank=True, null=True, editable=False)
    unsubscribing_reason = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Todos os usuários")

    def __str__(self) -> str:
        return str(self.email)

    @property
    def agreed(self):
        return bool(self.agreed_at)

    @property
    def refresh_token(self) -> str:
        return RefreshToken.for_user(self)

    @property
    def token(self) -> str:
        return str(self.refresh_token.access_token)

    @property
    def refresh(self) -> str:
        return str(self.refresh_token)

    def generate_token(self):
        self.hash_token = uuid.uuid4()
        self.save()

    @property
    def owner(self):
        return self

    @property
    def create_or_get_contact_id(self):
        first_name = self.name
        if first_name:
            first_name = str(self.name).split()[0]
        return ActiveCampaign.create_or_get_account(self.email, first_name, self.phone)
