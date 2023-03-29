# Generated by Django 4.1.7 on 2023-03-29 01:18

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("contents", "0002_article_cover_article_read_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                max_length=200,
                populate_from="title",
                unique=True,
                verbose_name="Slug",
            ),
        ),
    ]