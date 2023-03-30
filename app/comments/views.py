from rest_framework.viewsets import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from .serializers import (
    CommentSerializer,
    CreateCommentSerializer,
    CreateInteractionCommentSerializer,
)

from .models import Comment


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.actives()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        if article_id:
            return Comment.objects.actives().filter(article_id=article_id)
        return Comment.objects.actives()


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    queryset = Comment.objects.actives()
    permission_classes = (AllowAny,)


class CommentInteractionAPIView(generics.UpdateAPIView):
    serializer_class = CreateInteractionCommentSerializer
    queryset = Comment.objects.actives()
    permission_classes = (AllowAny,)

    def put(self, request, *args, **kwargs):
        return Response({"message": {"success"}}, status=200)
