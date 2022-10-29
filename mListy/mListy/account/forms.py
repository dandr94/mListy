from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import IntegrityError

from mListy.account.models import Profile
from mListy.account.validators import validate_only_letters_and_numbers

UserModel = get_user_model()


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        max_length=Profile.USERNAME_MAX_CHAR,
        validators=[MinLengthValidator(Profile.USERNAME_MIN_CHAR),
                    validate_only_letters_and_numbers]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            username=self.cleaned_data['username'],
            user=user
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class LoginAccountForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = ['username', 'password']