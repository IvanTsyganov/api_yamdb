from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# local
from api.v1.serializers import (ReviewSerializer, CommentSerializer)
from .permissions import IsAuthorOrAdminOrModerOrReadOnly
from .models import Title, Review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        return title_obj.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title_obj)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerOrReadOnly,)

    def get_queryset(self):
        review = Review.objects.get(id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review_obj = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review_obj)
