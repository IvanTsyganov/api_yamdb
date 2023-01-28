from random import randint

from django.core.mail import send_mail
from requests import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import filters, mixins, pagination, permissions, viewsets, status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenViewBase

# local
from reviews.models import Genre, Title, Category, Review, Comment, User

from .permissions import(
    is_authenticated_Or_ReadOnlyPermission,
    IsAuthorOrReadOnly,
    AdminPermission,
)

from .serializers import(
    GenreSerializer,
    TitleSerializer,
    CategorySerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer,
    SignUpSerializer,
    TokenSerializer
)


class GenreviewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (is_authenticated_Or_ReadOnlyPermission,)

    def perform_create(self, serializer):
        pass


class CategoryviewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (is_authenticated_Or_ReadOnlyPermission,)

    def perform_create(self, serializer):
        pass


class TitleviewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (is_authenticated_Or_ReadOnlyPermission,)

    def perform_create(self, serializer):
        pass


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
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return title.reviews


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review_obj = get_object_or_404(Review, id=review_id)
        return review_obj.comments


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code_confirm = str(randint(1001, 9999))
    user = User.objects.get_or_create(
        username=serializer.data.get('username'),
        email=serializer.data.get('email'),
        confirmation_code=code_confirm
    )
    send_mail(
        subject='Регистрация на сайте',
        message='Здравствуйте. Вы получили это сообщение, так как ваш адрес был использован'
        ' при регистрации нового пользователя на портале YamDB.'
        f'Ваш проверочный код: {code_confirm}',
        #serializer.initial_data['email'],
        recipient_list=[user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(TokenViewBase):
    serializer_class = TokenSerializer
