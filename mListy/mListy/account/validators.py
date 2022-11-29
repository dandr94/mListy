from django.core.exceptions import ValidationError

USERNAME_ERROR_MESSAGE = 'Username can contain only letters and numbers.'
NAME_ERROR_MESSAGE = 'Name can only contain letters.'


def validate_only_letters_and_numbers(value):
    if not value.isalnum():
        raise ValidationError(USERNAME_ERROR_MESSAGE)


def validate_only_letters(value):
    if not value.isalpha():
        raise ValidationError(NAME_ERROR_MESSAGE)
