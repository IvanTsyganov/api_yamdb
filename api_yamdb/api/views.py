from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import filters, mixins, pagination, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.shortcuts import get_object_or_404
# local
from reviews.models import Genre, Title, Category, Review, Comment
from users.models import User
from .permissions import (
    IsAuthenticatedOrReadOnlyPermission, IsAuthorOrReadOnly, IsAdminOrReadOnly
)
from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    GenreSerializer,
    TitleSerializer,
    CategorySerializer,
    UserSerializer,
    SignUpSerializer,
    ReadOnlyTitleSerializer,
)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    #permission_classes = (AllowAny ,)


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


