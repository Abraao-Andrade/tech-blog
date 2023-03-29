# Generated by Django 4.1.7 on 2023-03-29 02:15

import app.common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contents", "0003_video_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="photo",
            field=app.common.fields.ImageField(
                blank=True, null=True, upload_to="authors-profile", verbose_name="Foto"
            ),
        ),
    ]