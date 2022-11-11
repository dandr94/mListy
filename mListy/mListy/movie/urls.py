from django.urls import path

from mListy.movie.views import MovieDetailsView, AddMovieToListView

urlpatterns = [
    path('movie/details/<str:slug>/', MovieDetailsView.as_view(), name='details movie'),
    path('add-movie-to-list/<str:slug>/', AddMovieToListView.as_view(), name='add movie to list')

]
