from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms import ModelForm

from mListy.list.models import List


class CreateListForm(ModelForm):
    UNIQUE_TITLE_ERROR_MESSAGE = 'You already have a list with that title. Please choose another.'

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        user_list = super().save(commit=False)

        user_list.user = self.user
        if commit:
            user_list.save()

        return user_list

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')

        if List.objects.filter(title=title, user_id=self.user.id).exists():
            raise ValidationError(self.UNIQUE_TITLE_ERROR_MESSAGE)

    class Meta:
        model = List
        fields = ['title', 'cover']
