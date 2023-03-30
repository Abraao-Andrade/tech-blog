from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.comments"

    verbose_name = "Comentário"
    verbose_name_plural = "Comentários"
