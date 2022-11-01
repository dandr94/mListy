from django.urls import path

from mListy.list.views import CreateListView, EditListView, DeleteListView

urlpatterns = [
    path('create_list/', CreateListView.as_view(), name='create list'),
    path('list/edit/<str:slug>/', EditListView.as_view(), name='edit list'),
    path('list/delete/<str:slug>/', DeleteListView.as_view(), name='delete list')
]
