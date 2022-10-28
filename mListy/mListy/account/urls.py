from django.urls import path

from mListy.account.views import HomeViewNoProfile

urlpatterns = [
    path('', HomeViewNoProfile.as_view(), name='index')
]
