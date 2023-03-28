from rest_framework import serializers

from .models import Category, Author, Article, Video


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "description", "slug", "is_active"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "profession", "description", "photo", "is_active"]


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "subtitle",
            "text",
            "banner",
            "read_time",
            "author",
            "categories",
            "published_at",
            "is_active",
            "read_count",
            "show_in_start",
        ]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["url", "title", "description", "published_at", "is_active"]
