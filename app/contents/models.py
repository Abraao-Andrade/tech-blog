from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from app.common.models import TimeStampModel, SoftDeletionModel
from app.common.fields import ImageField
from .managers import CategoryManager, AuthorManager, ArticlesManager, VideoManager
from ckeditor.fields import RichTextField


class Category(TimeStampModel, SoftDeletionModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Nome"),
        help_text=_("Nome que será exibido para o usuário na listagem de categorias"),
        db_index=True,
        unique=True,
    )
    description = models.TextField(verbose_name=_("Descrição"), blank=True, null=True)
    slug = AutoSlugField(
        verbose_name=_("Slug"), populate_from="name", unique=True, max_length=100
    )
    is_active = models.BooleanField(
        verbose_name=_("Ativo?"),
        help_text=_("Indica se a categoria está ativa"),
        default=True,
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")

    def __str__(self) -> str:
        return self.name


class Author(TimeStampModel, SoftDeletionModel):
    name = models.CharField(max_length=400, verbose_name=_("Nome"))
    photo = ImageField(upload_to="authors-profile", verbose_name=_("Foto"))
    profession = models.CharField(
        max_length=255, verbose_name=_("Profissão"), blank=True, null=True
    )
    description = models.TextField(verbose_name=_("Descrição"), blank=True, null=True)
    is_active = models.BooleanField(
        verbose_name=_("Ativo?"),
        help_text=_("Indica se o autor está ativo"),
        default=True,
    )

    objects = AuthorManager()

    class Meta:
        verbose_name = _("Autor")
        verbose_name_plural = _("Autores")

    def __str__(self) -> str:
        return self.name


class Article(TimeStampModel, SoftDeletionModel):
    title = models.CharField(
        max_length=500, verbose_name=_("Título"), db_index=True, unique=True
    )
    slug = AutoSlugField(
        verbose_name=_("Slug"), populate_from="title", unique=True, max_length=200
    )
    subtitle = models.TextField(
        verbose_name=_("Subtítulo"),
        help_text=_("Exibido na visualização do card de artigos."),
        blank=True,
        null=True,
    )
    text = RichTextField(
        verbose_name=_("Texto do Artigo"), config_name="small", blank=True, null=True
    )
    banner = ImageField(
        upload_to="articles-images",
        help_text=_("Esta imagem será exibida como capa do artigo e banner"),
    )
    cover = ImageField(
        upload_to="articles-images",
        verbose_name=_("Imagem"),
        help_text=_("Esta imagem será exibida dentro do artigo."),
        blank=True,
        null=True,
    )
    read_time = models.TimeField(
        verbose_name=_("Templo de Leitura"), blank=True, null=True
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Autor"),
        blank=True,
        null=True,
    )
    categories = models.ManyToManyField(Category)
    published_at = models.DateTimeField(
        verbose_name=_("Publicar em"), blank=False, null=True
    )
    read_count = models.PositiveIntegerField(
        verbose_name=_("Visualizações"), default=0, editable=False
    )
    is_active = models.BooleanField(
        verbose_name=_("Ativo?"),
        help_text=_("Indica se o artigo está ativo"),
        default=True,
    )
    show_in_start = models.BooleanField(
        verbose_name=_("Exibir no inicio?"), default=False
    )

    objects = ArticlesManager()

    class Meta:
        verbose_name = _("Artigo")
        verbose_name_plural = _("Artigos")

    def __str__(self) -> str:
        return self.title


class Video(TimeStampModel):
    url = models.URLField(
        max_length=250,
        unique=False,
        error_messages={"unique": "Já existe um vídeo que utilizou esse link"},
    )
    title = models.CharField(
        max_length=400, verbose_name=_("Título"), blank=True, null=True
    )
    description = models.TextField(verbose_name=_("Descrição"), blank=True, null=True)
    published_at = models.DateTimeField(
        verbose_name=_("Publicar em"), blank=False, null=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Ativo?"),
        help_text=_("Indica se o artigo está ativo"),
        default=True,
    )

    objects = VideoManager()

    class Meta:
        verbose_name = _("Vídeo")
        verbose_name_plural = _("Vídeos")

    def __str__(self) -> str:
        return self.title
