import datetime
from rest_framework import serializers, exceptions
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
#local
from reviews.models import Category, Title, Genre, Review, Comment
from users.models import User
from api_yamdb.settings import (MESSAGE_FOR_RESERVED_NAME,
                                MESSAGE_FOR_USER_NOT_FOUND,
                                RESERVED_NAME)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    def validate_year(self,value):
        year_now = datetime.date.today().year
        if not (value <= year_now):
            raise serializers.ValidationError('Проверьте год выпуска')
        return value
    
    def validate_genre(self,value):
        if not Genre.objects.filter(name = f'{value}').exists():
            raise serializers.ValidationError('Выберите жанр из ранее созданных')
        return value
    
    def validate_category(self,value):
        if not Category.objects.filter(name = f'{value}').exists():
            raise serializers.ValidationError('Выберите категорию из ранее созданных')
        return value

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        
class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом user.
    Зарезервированное имя использовать нельзя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', )

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)
        return value


class ForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом admin.
    Зарезервированное имя использовать нельзя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена.
    Зарезервированное имя использовать нельзя."""
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(MESSAGE_FOR_USER_NOT_FOUND)
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')