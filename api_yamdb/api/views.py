from random import randint

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from requests import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import filters, mixins, pagination, permissions, viewsets, status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import filters, mixins, pagination, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response

# local
from reviews.models import Genre, Title, Category, User


from .permissions import(
    IsAuthenticatedOrReadOnlyPermission,
    IsAuthorOrReadOnly,
    AdminPermission,
    IsAdminOrReadOnly
)


from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    GenreSerializer,
    TitleSerializer,
    CategorySerializer,
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
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
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)


    @action(
        ['GET', 'PATCH'], permission_classes=(IsAuthenticated,),
        detail=False, url_path='me'
    )
    def me_user(self, request):
        if not request.data:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.user.role == 'admin':
            serializer.update(request.user, serializer.validated_data)
        else:
            serializer.nonadmin_update(
                request.user, serializer.validated_data
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title_obj)

    def partial_update(self, request, *args, **kwargs):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review_obj = get_object_or_404(Review, id=review_id)
        return review_obj.comments


def create_code_confirm_code_and_send_mail(username):

    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Confirmation code',
        message=f'Your confirmation code {confirmation_code}',
        from_email='admin@yamdb.xxx',
        recipient_list=[user.email]
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    create_code_confirm_code_and_send_mail(serializer.data['username'])
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(
            User, username=serializer.data['username'])
        if default_token_generator.check_token(
           user, serializer.data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK)
        return Response({
            'confirmation code': 'Некорректный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)
