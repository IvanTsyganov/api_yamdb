from reviews.models import Genre, Title, Category,User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, pagination, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
# local
from reviews.models import Genre, Title, Category, Review, Comment
from .permissions import (
    IsAuthenticatedOrReadOnlyPermission, IsAuthorOrReadOnly
)

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    GenreSerializer,
    TitleSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer,
)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleviewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnlyPermission,)
    filter_backends = [DjangoFilterBackend]
    filterset_class  = TitlesFilter

    def perform_create(self, serializer):
        pass


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        pass


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        pass
