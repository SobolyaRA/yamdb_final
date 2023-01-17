import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            "Username 'me' is not valid",
            params={'value': value}
        )

    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'Некорректное значение для поля year: {value}!'
        )
