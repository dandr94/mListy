from django.urls import path

from mListy.movie.views import MovieDetailsView, AddListEntryView, EditListEntryView, DeleteListEntryView

urlpatterns = [
    path('movie/details/<str:slug>/', MovieDetailsView.as_view(), name='details movie'),
    path('add-movie-to-list/<str:slug>/', AddListEntryView.as_view(), name='add movie to list'),
    path('edit/<int:pk>/<str:slug>/', EditListEntryView.as_view(), name='edit entry'),
    path('delete/<int:pk>/<str:slug>/', DeleteListEntryView.as_view(), name='delete entry')
]
