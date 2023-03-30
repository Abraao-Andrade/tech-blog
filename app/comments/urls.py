from django.urls import re_path

from .views import (
    CommentListAPIView,
    CommentCreateAPIView,
    CommentInteractionAPIView,
)

app_name = "comments"

urlpatterns = [
    re_path(
        r"^(?P<version>(v1))/comments/(?P<article_id>\d+)/article$",
        CommentListAPIView.as_view(),
        name="comments-article-list",
    ),
    re_path(
        r"^(?P<version>(v1))/comments/create$",
        CommentCreateAPIView.as_view(),
        name="comments-create",
    ),
    re_path(
        r"^(?P<version>(v1))/comments/(?P<pk>\d+)/interaction$",
        CommentInteractionAPIView.as_view(),
        name="comments-interaction",
    ),
]
