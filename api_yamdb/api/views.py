from django.core.mail import send_mail
from rest_framework import filters, mixins, pagination, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from reviews.models import Genre, Title, Category, User
from .permissions import is_authenticated_Or_ReadOnlyPermission

from rest_framework import filters, mixins, pagination, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
# local
from reviews.models import Genre, Title, Category, Review, Comment
from .permissions import (
    is_authenticated_Or_ReadOnlyPermission, IsAuthorOrReadOnly
)

from .serializers import (
    GenreSerializer,
    TitleSerializer,
    CategorySerializer,
    UserSerializer,
    SignUpSerializer
    ReviewSerializer,
    CommentSerializer,
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
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    #permission_classes = (AllowAny ,)


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


'''
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(username=request.data['username'],
                               email=request.data['email']).exists():
        serializer.save()
    user = User.objects.get(username=request.data['username'],
                            email=request.data['email'])
    conformation_code = default_token_generator.make_token(user)
    send_mail(f'Hello, {str(user.username)}! Your code is here!',
              conformation_code,
              settings.EMAIL_FOR_AUTH_LETTERS,
              [request.data['email']],
              fail_silently=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
'''


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
