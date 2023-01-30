from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )

    first_name = models.EmailField(
        max_length=150,
        null=True
    )

    last_name = models.EmailField(
        max_length=150,
        null=True
    )

    role = models.CharField(
        choices=USER_ROLES,
        max_length=50,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def str(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название категории',
                            help_text='Укажите название для категории')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='URL категории',
                            help_text='Задайте уникальный URL адрес категории')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра',
                            help_text='Задайте название жанра')
    slug = models.SlugField(max_length=50,
                            verbose_name='URL жанра',
                            help_text='Задайте уникальный URL адрес жанра.',
                            unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения',
                            help_text='Укажите название произведения')
    year = models.IntegerField(verbose_name='Год выпуска',
                               help_text='Укажите год выпуска произведения')
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Описание произведения')
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр произведения',
                                   related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        null=True,
        default=None,
        verbose_name='Рейтинг произведения'
    )

    def __str__(self):
        return self.name



class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор обзора',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            ),
        )

        
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-pub_date',)
