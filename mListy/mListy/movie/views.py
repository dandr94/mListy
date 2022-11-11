from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from mListy.list.models import List
from mListy.movie.forms import AddMovieToListForm
from mListy.movie.models import MovieDB


class AddMovieToListView(CreateView):
    template_name = 'movie/add_movie_to_list.html'
    form_class = AddMovieToListForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['user_lists'] = List.objects.filter(user_id=self.request.user.id)
        movie_id = self.kwargs['slug'].split('-')[0]
        kwargs['movie'] = MovieDB.objects.get(movie_id=movie_id)

        return kwargs

    def get_success_url(self):
        return reverse_lazy('details movie', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_slug'] = self.kwargs['slug']
        return context


class MovieDetailsView(LoginRequiredMixin, DetailView):
    model = MovieDB
    template_name = 'movie/details_movie.html'
    context_object_name = 'movie'
