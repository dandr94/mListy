from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from mListy.list.models import List, ListEntry
from mListy.movie.forms import AddMovieToListForm, EditListEntryForm, DeleteListEntryForm
from mListy.movie.models import MovieDB


class AddListEntryView(CreateView):
    template_name = 'movie/add_movie_to_list.html'
    form_class = AddMovieToListForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['user_lists'] = List.objects.filter(user_id=self.request.user.id)
        kwargs['movie'] = MovieDB.objects.get(slug=self.kwargs['slug'])

        return kwargs

    def get_success_url(self):
        return reverse_lazy('details movie', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_slug'] = self.kwargs['slug']
        return context


class EditListEntryView(LoginRequiredMixin, UpdateView):
    model = ListEntry
    template_name = 'movie/edit_entry.html'
    form_class = EditListEntryForm
    context_object_name = 'entry'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_lists'] = List.objects.filter(user_id=self.request.user.id)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('details list', kwargs={'str': self.request.user.username, 'slug': self.object.list.slug})


class DeleteListEntryView(DeleteView):
    model = ListEntry
    template_name = 'movie/delete_entry.html'
    context_object_name = 'entry'
    form_class = DeleteListEntryForm

    def get_success_url(self):
        return reverse_lazy('details list', kwargs={'str': self.request.user.username, 'slug': self.object.list.slug})


class MovieDetailsView(LoginRequiredMixin, DetailView):
    model = MovieDB
    template_name = 'movie/details_movie.html'
    context_object_name = 'movie'
