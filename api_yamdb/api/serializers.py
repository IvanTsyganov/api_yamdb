import datetime
from rest_framework import serializers, exceptions
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

# local
from reviews.models import Category, Title, Genre, User, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    def validate_year(self, value):
        year_now = datetime.date.today().year
        if not (value <= year_now):
            raise serializers.ValidationError('Проверьте год выпуска')
        return value

    def validate_genre(self, value):
        if not Genre.objects.filter(name=f'{value}').exists():
            raise serializers.ValidationError('Выберите жанр из ранее созданных')
        return value

    def validate_category(self, value):
        if not Category.objects.filter(name=f'{value}').exists():
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

    def nonadmin_update(self, instance, validated_data):
        validated_data.pop('role', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'first_name', 'last_name',
            'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SignUpSerializer(Serializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value.lower() == 'me' and '^[\w.@+-]+\z' not in value:
            raise serializers.ValidationError('Недопустимое имя пользователя!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if value.lower() == 'me' and '^[\w.@+-]+\z' not in value:
            raise serializers.ValidationError('Недопустимое имя пользователя!')
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound('Пользователя не существует!')
        return value


class AdminSerializer(serializers.Serializer):
    pass