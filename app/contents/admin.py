from django.contrib import admin
from .models import Category, Author, Article, Video
from .forms import ArticleAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active"]
    list_filter = [
        "is_active",
    ]
    search_fields = ["name"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = [
        "is_active",
    ]
    search_fields = ["name"]


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category_list", "is_active"]
    list_filter = ["is_active", "author", "categories"]
    search_fields = ["title", "author"]
    form = ArticleAdminForm
    readonly_fields = [
        "read_count",
    ]
    fieldsets = [
        (
            None,
            {
                "classes": (
                    "suit-tab",
                    "suit-tab-general",
                ),
                "fields": [
                    "title",
                    "subtitle",
                    "banner",
                    "cover",
                    "text",
                    "categories",
                    "author",
                    "read_count",
                ],
            },
        ),
        (
            "Configuração",
            {
                "classes": (
                    "suit-tab",
                    "suit-tab-general",
                ),
                "fields": [
                    "published_at",
                    "read_time",
                    "is_active",
                    "show_in_start",
                ],
            },
        ),
    ]

    def category_list(self, obj):
        return ", ".join(o.name for o in obj.categories.all())

    category_list.short_description = "Categorias"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "published_at", "is_active"]
    list_filter = [
        "is_active",
    ]
    search_fields = ["title", "url"]
