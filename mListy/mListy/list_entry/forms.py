from django.core.exceptions import ValidationError
from django.forms import ModelForm

from mListy.list_entry.models import ListEntry
from mListy.movie.mixins import CssStyleFormMixin


class AddListEntryForm(ModelForm, CssStyleFormMixin):
    def __init__(self, user, user_lists, movie, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()
        self.user = user
        self.user_lists = user_lists
        self.movie = movie
        self.fields['list'].queryset = self.user_lists

    def save(self, commit=True):
        entry = super().save(commit=False)
        entry.movie = self.movie
        entry.would_recommend = self.cleaned_data['would_recommend']
        entry.grade = self.cleaned_data['grade']
        entry.list = self.cleaned_data['list']

        if commit:
            entry.save()

        return entry

    def clean(self):
        cleaned_data = super().clean()

        user_list = cleaned_data.get('list')

        exists = ListEntry.objects.filter(movie__id=self.movie.id, list__title=user_list).exists()

        if exists:
            raise ValidationError(f'{self.movie.name} is already in {user_list}.')

    class Meta:
        model = ListEntry
        fields = ['grade', 'list', 'would_recommend', 'status']


class EditListEntryForm(ModelForm, CssStyleFormMixin):
    def __init__(self, user_lists, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()
        self.fields['list'].queryset = user_lists

    class Meta:
        model = ListEntry
        fields = ['grade', 'list', 'would_recommend', 'status']


class DeleteListEntryForm(ModelForm, CssStyleFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = ListEntry
        fields = []