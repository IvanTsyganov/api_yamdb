from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def __str__(self):
        return self.username
