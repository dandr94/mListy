from django.urls import path
from mListy.list_entry.views import AddListEntryView, EditListEntryView, DeleteListEntryView

urlpatterns = [
    path('add/<str:slug>/', AddListEntryView.as_view(), name='add entry'),
    path('edit/<int:pk>/<str:slug>/', EditListEntryView.as_view(), name='edit entry'),
    path('delete/<int:pk>/<str:slug>/', DeleteListEntryView.as_view(), name='delete entry')
]
