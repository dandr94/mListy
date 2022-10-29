from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.core.validators import MinLengthValidator
from django.db import models

from mListy.account.managers import mListyUserManager
from mListy.account.validators import validate_only_letters_and_numbers, validate_only_letters


class mListyUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LEN = 15
    USERNAME_MIN_LEN = 2
    USERNAME_UNIQUE_ERROR_MESSAGE = 'Username is not available'

    EMAIL_UNIQUE_ERROR_MESSAGE = 'This email is already used'

    username = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=USERNAME_MAX_LEN,
        validators=[MinLengthValidator(USERNAME_MIN_LEN),
                    validate_only_letters_and_numbers],
        error_messages={
            'unique': USERNAME_UNIQUE_ERROR_MESSAGE
        }
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        error_messages={
            'unique': EMAIL_UNIQUE_ERROR_MESSAGE
        }

    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_superuser = models.BooleanField(
        default=False
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = mListyUserManager()


class Profile(models.Model):
    FIRST_NAME_MAX_CHAR = 15
    FIRST_NAME_MIN_CHAR = 2

    LAST_NAME_MAX_CHAR = 15
    LAST_NAME_MIN_CHAR = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_CHAR,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(FIRST_NAME_MIN_CHAR),
            validate_only_letters
        ]

    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_CHAR,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(LAST_NAME_MIN_CHAR),
            validate_only_letters
        ]
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    twitter = models.URLField(
        blank=True,
        null=True,
    )

    instagram = models.URLField(
        blank=True,
        null=True,
    )

    facebook = models.URLField(
        blank=True,
        null=True,
    )

    user = models.OneToOneField(mListyUser, on_delete=models.CASCADE, primary_key=True)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
