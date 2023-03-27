from django.db import models
from django.utils import timezone


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def actives(self):
        return self.get_queryset().filter(is_active=True)


class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def actives(self):
        return self.get_queryset().filter(is_active=True)


class ArticlesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def actives(self):
        return self.get_queryset().filter(
            published_at__lte=timezone.now(), is_active=True
        )


class VideoManager(models.Manager):
    def actives(self):
        return (
            super()
            .get_queryset()
            .filter(published_at__lte=timezone.now(), is_active=True)
        )
