# Generated by Django 4.1.7 on 2023-03-29 02:15

import app.common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contents", "0004_alter_author_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="banner",
            field=app.common.fields.ImageField(
                blank=True,
                help_text="Esta imagem será exibida como capa do artigo e banner",
                null=True,
                upload_to="articles-images",
            ),
        ),
    ]
