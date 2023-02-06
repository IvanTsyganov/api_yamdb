from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            (f'Год {value} не может быть больше текущего!'),
            params={'value': value},
        )
