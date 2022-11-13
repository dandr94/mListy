from django.urls import path

from mListy.movie.views import MovieDetailsView, AddListEntryView, EditListEntryView, DeleteListEntryView

urlpatterns = [
    path('movie/details/<str:slug>/', MovieDetailsView.as_view(), name='details movie'),

    path('add/<str:slug>/', AddListEntryView.as_view(), name='add entry'),
    path('edit/<int:pk>/<str:slug>/', EditListEntryView.as_view(), name='edit entry'),
    path('delete/<int:pk>/<str:slug>/', DeleteListEntryView.as_view(), name='delete entry')
]
