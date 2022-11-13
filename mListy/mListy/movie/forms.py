from django.forms import ModelForm

from mListy.list.models import ListEntry


class AddMovieToListForm(ModelForm):
    def __init__(self, user, user_lists, movie, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.user_lists = user_lists
        self.movie = movie
        self.fields['list'].queryset = self.user_lists

    def save(self, commit=True):
        entry = super().save(commit=False)
        entry.movie_id = self.movie.movie_id
        entry.movie_name = self.movie.name
        entry.user = self.user
        entry.would_recommend = self.cleaned_data['would_recommend']
        entry.grade = self.cleaned_data['grade']
        entry.list = self.cleaned_data['list']

        if commit:
            entry.save()

        return entry

    class Meta:
        model = ListEntry
        fields = ['grade', 'list', 'would_recommend']


class EditListEntryForm(ModelForm):
    def __init__(self, user_lists, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.instance.user
        self.fields['list'].queryset = user_lists

    class Meta:
        model = ListEntry
        fields = ['grade', 'list', 'would_recommend']


class DeleteListEntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = ListEntry
        fields = []
