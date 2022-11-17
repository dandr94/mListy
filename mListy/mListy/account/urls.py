from django.urls import path

from mListy.account.views.auth import RegisterUserView, LoginUserView, LogoutUserView
from mListy.account.views.generic import HomeViewNoProfile, Dashboard
from mListy.account.views.profile import ProfileDetailsView, EditProfileView, ChangeUserPasswordView

urlpatterns = [
    path('', HomeViewNoProfile.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('change_password/', ChangeUserPasswordView.as_view(), name='change password'),

    path('profile/<str:slug>/', ProfileDetailsView.as_view(), name='details profile'),
    path('profile/edit/<str:slug>/', EditProfileView.as_view(), name='edit profile')
]
