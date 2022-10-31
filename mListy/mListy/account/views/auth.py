from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from mListy.account.forms import CreateUserForm, LoginAccountForm


class RegisterUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class LoginUserView(LoginView):
    form_class = LoginAccountForm
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


class LogoutUserView(LogoutView):
    pass
