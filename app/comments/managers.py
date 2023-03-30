from django.db import models


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def actives(self):
        return self.get_queryset().filter(status="published")
