from django.shortcuts import get_object_or_404
from rest_framework.viewsets import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    CategorySerializer,
    ArticleSerializer,
    VideoSerializer,
)

from .models import (
    Category,
    Article,
    Video,
)

from .tasks import handle_update_article_read_count


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.actives()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.actives()


class CategoryRetreiveAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.actives()
    permission_classes = (AllowAny,)

    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        if category:
            return Response(
                CategorySerializer(
                    category, many=False, context={"request": request}
                ).data
            )
        return Response("category not found", status=status.HTTP_200_OK)


class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.actives()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Article.objects.actives()


class ArticlesMostReadListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.most_read()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Article.objects.most_read()


class ArticleRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.actives()
    permission_classes = (AllowAny,)

    def get(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug)
        if article:
            handle_update_article_read_count.delay(article.pk)
            return Response(
                ArticleSerializer(
                    article, many=False, context={"request": request}
                ).data
            )
        return Response("article not found", status=status.HTTP_200_OK)


class CategoryContentListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.actives()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category_slug = self.kwargs.get("slug")

        if category := Category.objects.filter(slug=category_slug).first():
            return Article.objects.filter(categories__in=[category.pk])
        return Category.objects.filter(slug=category_slug)


class VideoListAPIView(generics.ListAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.actives()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Video.objects.actives()


class VideoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.actives()
    permission_classes = (AllowAny,)

    def get(self, request, slug, *args, **kwargs):
        video = get_object_or_404(Video, slug=slug)
        if video:
            return Response(
                VideoSerializer(video, many=False, context={"request": request}).data
            )
        return Response("video not found", status=status.HTTP_200_OK)
