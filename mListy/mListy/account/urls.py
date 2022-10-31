from django.urls import path

from mListy.account.views import HomeViewNoProfile, RegisterUserView, LoginUserView, LogoutUserView, ProfileDetailsView

urlpatterns = [
    path('', HomeViewNoProfile.as_view(), name='index'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    path('profile/<str:slug>/', ProfileDetailsView.as_view(), name='profile details')
]
