from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError

from mListy.account.models import Profile
from mListy.movie.mixins import CssStyleFormMixin
from django.forms import ModelForm

UserModel = get_user_model()


class CreateUserForm(UserCreationForm, CssStyleFormMixin):
    FIELD_NAME_HELP_TEXT_TO_IGNORE = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()
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


class LoginAccountForm(AuthenticationForm, CssStyleFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    class Meta:
        model = UserModel
        fields = ['username', 'password']


class EditProfileForm(CssStyleFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['slug', 'user']


class ChangePasswordForm(CssStyleFormMixin, PasswordChangeForm):
    FIELD_NAME_HELP_TEXT_TO_IGNORE = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()
        for field_name in self.FIELD_NAME_HELP_TEXT_TO_IGNORE:
            self.fields[field_name].help_text = None

    class Meta:
        model = Profile
        fields = ['old_password', 'new_password1', 'new_password2']


class ResetPasswordForm(PasswordResetForm, CssStyleFormMixin):
    EMAIL_DO_NOT_EXIST_ERROR_MESSAGE = 'Wrong email. This email is not being used. Please enter a valid email.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        exists = UserModel.objects.filter(email=email).exists()

        if not exists:
            raise ValidationError(self.EMAIL_DO_NOT_EXIST_ERROR_MESSAGE)


class ResetPasswordConfirmForm(SetPasswordForm, CssStyleFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()
