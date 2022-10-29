from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.core.validators import MinLengthValidator
from django.db import models

from mListy.account.managers import mListyUserManager
from mListy.account.validators import validate_only_letters_and_numbers, validate_only_letters


User

class mListyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False

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

    USERNAME_FIELD = 'email'

    objects = mListyUserManager()


class Profile(models.Model):
    USERNAME_MAX_CHAR = 15
    USERNAME_MIN_CHAR = 2

    FIRST_NAME_MAX_CHAR = 15
    FIRST_NAME_MIN_CHAR = 2

    LAST_NAME_MAX_CHAR = 15
    LAST_NAME_MIN_CHAR = 2

    username = models.CharField(
        max_length=USERNAME_MAX_CHAR,
        validators=[
            MinLengthValidator(USERNAME_MIN_CHAR),
            validate_only_letters_and_numbers,
        ]
    )

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

    def __str__(self):
        return self.username
