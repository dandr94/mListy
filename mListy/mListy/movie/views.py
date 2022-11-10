from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from mListy.movie.models import MovieDB


class MovieDetailsView(LoginRequiredMixin, DetailView):
    model = MovieDB
    template_name = 'movie/details_movie.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context