from django.urls import path

from mListy.list.views import CreateListView, EditListView

urlpatterns = [
    path('create_list/', CreateListView.as_view(), name='create list'),
    path('list/edit/<str:slug>/', EditListView.as_view(), name='edit list')
]
