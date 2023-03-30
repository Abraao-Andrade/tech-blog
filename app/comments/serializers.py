from rest_framework import serializers

from .models import Comment
from app.contents.models import Article
from app.contents.serializers import ArticleSerializer
from .tasks import handle_update_comment_interaction


class ChildCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "text",
            "status",
            "parent",
            "article",
            "like",
            "spam",
            "created_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(many=False)
    child = ChildCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "text",
            "status",
            "parent",
            "article",
            "like",
            "spam",
            "created_at",
            "child",
        ]


class CreateCommentSerializer(serializers.ModelSerializer):
    article_id = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        source="article",
        queryset=Article.objects.all(),
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        many=False,
        required=False,
        write_only=True,
        source="parent",
        queryset=Comment.objects.all(),
    )
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    status = serializers.CharField(read_only=True)
    like = serializers.BooleanField(required=False)
    spam = serializers.BooleanField(required=False)

    class Meta:
        model = Comment
        fields = "__all__"

    def update(self, instance, validated_data):
        if validated_data.get("like"):
            instance.like += 1
            instance.save()
        if validated_data.get("spam"):
            instance.spam += 1
            instance.save()
        return super().update(instance, validated_data)


class CreateInteractionCommentSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(required=False)
    spam = serializers.BooleanField(required=False)

    class Meta:
        model = Comment
        fields = "__all__"

    def update(self, instance, validated_data):
        return handle_update_comment_interaction.delay(
            comment_id=instance.id,
            like=validated_data.get("like", None),
            spam=validated_data.get("spam", None),
        )
