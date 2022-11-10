from django.urls import path

from mListy.movie.views import MovieDetailsView

urlpatterns = [
    path('movie/details/<str:slug>', MovieDetailsView.as_view(), name='details movie')

]
