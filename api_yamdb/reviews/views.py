from rest_framework import permissions, viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# local
from reviews.models import Title, Review, Comment
from reviews.permissions import (
    IsAuthorOrAdministratorOrReadOnly
)
from api.serializers import (ReviewSerializer, CommentSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title_obj)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = Review.objects.get(id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_obj = get_object_or_404(Review, id=review_id)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, title=title_obj)
