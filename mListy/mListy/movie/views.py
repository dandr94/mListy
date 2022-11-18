from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from mListy.list.models import List, ListEntry
from mListy.movie.forms import AddListEntryForm, EditListEntryForm, DeleteListEntryForm
from mListy.movie.helpers import check_if_in_db, add_movie_to_db, return_youtube_trailer
from mListy.movie.models import MovieDB
import tmdbsimple as tmdb


class AddListEntryView(CreateView):
    template_name = 'movie/add_entry.html'
    form_class = AddListEntryForm

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

    def dispatch(self, request, *args, **kwargs):
        movie_id = kwargs['slug'].split('-')[0]
        exists = check_if_in_db(movie_id)
        if not exists:
            add_movie_to_db(movie_id)
        kwargs['movie'] = exists
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['youtube_trailer'] = return_youtube_trailer(context['movie'].name, str(context['movie'].release_date.year))
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
