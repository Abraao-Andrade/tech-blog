from django.db import models
from django.utils.translation import gettext_lazy as _
from app.common.models import TimeStampModel, SoftDeletionModel
from app.common import choices


class Comment(TimeStampModel, SoftDeletionModel):
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("Nome do Usuário"),
    )
    email = models.EmailField(blank=True, null=True, editable=False)
    text = models.TextField(editable=False, verbose_name=_("Comentario"))
    status = models.CharField(
        max_length=50, choices=choices.STATUS_COMMENT, default="published", blank=True
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=True,
        verbose_name="Resposta",
    )
    article = models.ForeignKey(
        "contents.Article",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False,
        verbose_name="Artigo Relacionado",
    )

    like = models.PositiveIntegerField(default=0, editable=False)
    spam = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = _("Comentário")
        verbose_name_plural = _("Comentários")

    def __str__(self) -> str:
        return self.text
