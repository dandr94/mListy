from django.urls import path

from mListy.movie.views import MovieDetailsView, SearchMovieView

urlpatterns = [
    path('movie/details/<str:slug>/', MovieDetailsView.as_view(), name='details movie'),
    path('search/', SearchMovieView.as_view(), name='search movie'),
]
