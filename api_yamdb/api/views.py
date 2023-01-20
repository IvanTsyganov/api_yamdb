from reviews.models import Genre, Title, Category
from rest_framework import filters, mixins, pagination, permissions, viewsets

from .permissions import is_authenticated_Or_ReadOnlyPermission
from .serializers import (
    GenreSerializer,
    TitleSerializer,
    CategorySerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (is_authenticated_Or_ReadOnlyPermission,)

    def perform_create(self, serializer):
        pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (is_authenticated_Or_ReadOnlyPermission,)

    def perform_create(self, serializer):
        pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (is_authenticated_Or_ReadOnlyPermission,)

    def perform_create(self, serializer):
        pass
