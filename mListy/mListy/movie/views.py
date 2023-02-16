from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from mListy.movie.helpers import check_if_in_db, add_movie_to_db, return_youtube_trailer, return_similar_movies
from mListy.movie.models import MovieDB
import tmdbsimple as tmdb
from helpers import TMDB_IMG_PATH


class MovieDetailsView(LoginRequiredMixin, DetailView):
    model = MovieDB
    template_name = 'movie/details_movie.html'
    context_object_name = 'movie'

    def dispatch(self, request, *args, **kwargs):
        movie_id = kwargs['slug'].split('-')[0]

        try:
            exists = check_if_in_db(movie_id)
        except ValueError:
            raise Http404

        if not exists:
            add_movie_to_db(movie_id)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['youtube_trailer'] = return_youtube_trailer(context['movie'].name,
                                                            str(context['movie'].release_date.year))

        # TODO: Find why Avengers:Endgame gives error
        context['similar_movies'] = return_similar_movies(context['movie'].movie_id)
        return context


class SearchMovieView(LoginRequiredMixin, ListView):
    template_name = 'movie/search_movie.html'

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('search', '')

        if not keyword:
            return render(request, self.template_name)

        search_params = {
            'query': keyword,
            'page': 1,
            'include_adult': False
        }
        search = tmdb.Search()
        response = search.movie(**search_params)
        movies = []

        for item in response['results']:
            if not item['release_date'] or not item['poster_path']:
                continue
            item_result = {
                'title': item['title'],
                'vote_average': item['vote_average'],
                'image': TMDB_IMG_PATH + item['poster_path'],
                'slug': slugify(str(item['id']) + '-' + item['title'])
            }

            movies.append(item_result)

        context = {
            'movies': movies,
        }

        return render(request, self.template_name, context)
