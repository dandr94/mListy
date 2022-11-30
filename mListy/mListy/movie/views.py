from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from mListy.movie.helpers import check_if_in_db, add_movie_to_db, return_youtube_trailer
from mListy.movie.models import MovieDB
import tmdbsimple as tmdb


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
        return context


class SearchMovieView(LoginRequiredMixin, ListView):
    template_name = 'movie/search_movie.html'
    IMG_PATH = 'https://image.tmdb.org/t/p/w500/'
    IMG_NOT_FOUND = 'https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png'

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
            item_result = {
                'title': item['title'],
                'vote_average': item['vote_average'],
                'image': self.IMG_PATH + item['poster_path'] if item['poster_path'] else self.IMG_NOT_FOUND,
                'slug': slugify(str(item['id']) + '-' + item['title'])
            }

            movies.append(item_result)

        context = {
            'movies': movies,
        }

        return render(request, self.template_name, context)
