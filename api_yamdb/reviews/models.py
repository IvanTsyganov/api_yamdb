from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)
 
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    def __str__(self):
        return self.name



class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
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

    def str(self):
        return self.username
