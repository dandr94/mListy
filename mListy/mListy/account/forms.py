from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from mListy.account.models import Profile

UserModel = get_user_model()


class CreateUserForm(UserCreationForm):
    FIELD_NAME_HELP_TEXT_TO_IGNORE = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.FIELD_NAME_HELP_TEXT_TO_IGNORE:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
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