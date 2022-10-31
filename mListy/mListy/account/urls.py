from django.urls import path

from mListy.account.views.auth import RegisterUserView, LoginUserView, LogoutUserView
from mListy.account.views.generic import HomeViewNoProfile, Dashboard
from mListy.account.views.profile import ProfileDetailsView

urlpatterns = [
    path('', HomeViewNoProfile.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    path('profile/<str:slug>/', ProfileDetailsView.as_view(), name='profile details')
]
