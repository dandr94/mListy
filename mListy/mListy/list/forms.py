from django.core.exceptions import ValidationError
from django.forms import ModelForm
from mListy.movie.mixins import CssStyleFormMixin
from mListy.list.models import List

UNIQUE_TITLE_ERROR_MESSAGE = 'You already have a list with that title. Please choose another.'


class CreateListForm(ModelForm, CssStyleFormMixin):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_css_style_form_controls()

    def save(self, commit=True):
        user_list = super().save(commit=False)

        user_list.user = self.user
        if commit:
            user_list.save()

        return user_list

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')

        if List.objects.filter(title=title, user_id=self.user.pk).exists():
            raise ValidationError(UNIQUE_TITLE_ERROR_MESSAGE)

    class Meta:
        model = List
        fields = ['title', 'cover']


class EditListForm(ModelForm, CssStyleFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')

        if List.objects.filter(title=title, user_id=self.instance.user_id).exists():
            raise ValidationError(UNIQUE_TITLE_ERROR_MESSAGE)

    class Meta:
        model = List
        exclude = ['user', 'slug']


class DeleteListForm(ModelForm, CssStyleFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = List
        fields = []
