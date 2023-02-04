from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_year
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название категории',
        help_text='Укажите название для категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='URL категории',
        help_text='Задайте уникальный URL адрес категории'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Задайте название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='URL жанра',
        help_text='Задайте уникальный URL адрес жанра.',
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='Укажите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Укажите год выпуска произведения',
        validators=(validate_year,)
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
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

    def __str__(self):
        return self.name


class ReviewCommentAbstract(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Review(ReviewCommentAbstract):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг',
    )

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(ReviewCommentAbstract):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
