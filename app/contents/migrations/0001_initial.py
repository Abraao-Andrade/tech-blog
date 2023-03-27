# Generated by Django 4.1.7 on 2023-03-27 23:30

import app.common.fields
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, db_index=True, verbose_name="Modificado em"
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                ("name", models.CharField(max_length=400, verbose_name="Nome")),
                ("photo", app.common.fields.ImageField(upload_to="authors-profile")),
                (
                    "profession",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Profissão"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Descrição"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Indica se o autor está ativo",
                        verbose_name="Ativo?",
                    ),
                ),
            ],
            options={
                "verbose_name": "Autor",
                "verbose_name_plural": "Autores",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, db_index=True, verbose_name="Modificado em"
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="Nome que será exibido para o usuário na listagem de categorias",
                        max_length=255,
                        unique=True,
                        verbose_name="Nome",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Descrição"),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        max_length=100,
                        populate_from="name",
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Indica se a categoria está ativa",
                        verbose_name="Ativo?",
                    ),
                ),
            ],
            options={
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, db_index=True, verbose_name="Modificado em"
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        error_messages={
                            "unique": "Já existe um vídeo que utilizou esse link"
                        },
                        max_length=250,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=400, null=True, verbose_name="Título"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Descrição"),
                ),
                (
                    "published_at",
                    models.DateTimeField(null=True, verbose_name="Publicar em"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Indica se o artigo está ativo",
                        verbose_name="Ativo?",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vídeo",
                "verbose_name_plural": "Vídeos",
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "updated_at",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, db_index=True, verbose_name="Modificado em"
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                (
                    "title",
                    models.CharField(
                        db_index=True,
                        max_length=500,
                        unique=True,
                        verbose_name="Título",
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        max_length=200,
                        populate_from="title",
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "subtitle",
                    models.TextField(
                        blank=True,
                        help_text="Exibido na visualização do card de artigos.",
                        null=True,
                        verbose_name="Subtítulo",
                    ),
                ),
                (
                    "text",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name="Texto do Artigo"
                    ),
                ),
                ("banner", app.common.fields.ImageField(upload_to="articles-images")),
                (
                    "read_time",
                    models.TimeField(
                        blank=True, null=True, verbose_name="Templo de Leitura"
                    ),
                ),
                (
                    "published_at",
                    models.DateTimeField(null=True, verbose_name="Publicar em"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Indica se o artigo está ativo",
                        verbose_name="Ativo?",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="contents.author",
                        verbose_name="Autor",
                    ),
                ),
                ("categories", models.ManyToManyField(to="contents.category")),
            ],
            options={
                "verbose_name": "Artigo",
                "verbose_name_plural": "Artigos",
            },
        ),
    ]
