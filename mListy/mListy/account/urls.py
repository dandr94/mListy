from django.urls import path
from mListy.account.views.auth import RegisterUserView, LoginUserView, LogoutUserView, ResetPasswordView, \
    ResetPasswordCompleteView, ResetPasswordConfirmView, ResetPasswordDoneView
from mListy.account.views.generic import HomeViewNoProfile, Dashboard, About
from mListy.account.views.profile import ProfileDetailsView, EditProfileView, ChangePasswordView


urlpatterns = [
    # Generic
    path('', HomeViewNoProfile.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('about/', About.as_view(), name='about'),

    # Auth
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_sent/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', ResetPasswordCompleteView.as_view(), name='password_reset_complete'),

    # Profile
    path('profile/<str:slug>/', ProfileDetailsView.as_view(), name='details profile'),
    path('profile/edit/<str:slug>/', EditProfileView.as_view(), name='edit profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change password'),

]
