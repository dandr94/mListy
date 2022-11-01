from django.urls import path

from mListy.list.views import CreateListView

urlpatterns = [
    path('create_list/', CreateListView.as_view(), name='create list')
]
