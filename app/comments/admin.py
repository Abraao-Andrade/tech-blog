from django.contrib import admin
from .models import Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    verbose_name = "Resposta"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "email",
        "status",
        "article",
        "created_at",
    ]
    readonly_fields = [
        "name",
        "email",
        "text",
        "article",
        "created_at",
        "id",
        "like",
        "spam",
        "parent",
    ]
    search_fields = ["text", "name", "email"]
    list_filter = [
        "article",
    ]
    inlines = [
        CommentInline,
    ]
    fieldsets = (
        (
            "Pergunta",
            {
                "fields": (
                    "id",
                    "name",
                    "email",
                    "text",
                    "article",
                    "created_at",
                    "parent",
                    "status",
                    "like",
                    "spam",
                )
            },
        ),
    )
