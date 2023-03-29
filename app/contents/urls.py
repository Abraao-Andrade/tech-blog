from django.urls import re_path

from .views import (
    CategoryListAPIView,
    CategoryContentListAPIView,
    ArticleListAPIView,
    ArticleRetrieveAPIView,
    ArticlesMostReadListAPIView,
    VideoListAPIView,
    VideoRetrieveAPIView,
    BannersListAPIView,
)

app_name = "contents"

urlpatterns = [
    re_path(
        r"^(?P<version>(v1))/categories$",
        CategoryListAPIView.as_view(),
        name="categories-list",
    ),
    re_path(
        r"^(?P<version>(v1))/categories/(?P<slug>[-\w]+)/contents$",
        CategoryContentListAPIView.as_view(),
        name="category-contents-list",
    ),
    re_path(
        r"^(?P<version>(v1))/articles$",
        ArticleListAPIView.as_view(),
        name="articles-list",
    ),
    re_path(
        r"^(?P<version>(v1))/articles/(?P<slug>[-\w]+)/article$",
        ArticleRetrieveAPIView.as_view(),
        name="article-retrieve",
    ),
    re_path(
        r"^(?P<version>(v1))/articles/most-read$",
        ArticlesMostReadListAPIView.as_view(),
        name="articles-most-read-list",
    ),
    re_path(
        r"^(?P<version>(v1))/videos$",
        VideoListAPIView.as_view(),
        name="videos-list",
    ),
    re_path(
        r"^(?P<version>(v1))/videos/(?P<slug>[-\w]+)/video$",
        VideoRetrieveAPIView.as_view(),
        name="video-retrieve",
    ),
    re_path(
        r"^(?P<version>(v1))/banners$",
        BannersListAPIView.as_view(),
        name="banners-list",
    ),
]
