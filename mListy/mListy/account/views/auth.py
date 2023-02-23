from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.http import url_has_allowed_host_and_scheme
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
        next_url = self.request.POST.get('next', '')

        if next_url and url_has_allowed_host_and_scheme(next_url, None):
            return next_url
        else:
            return super().get_success_url()


class LogoutUserView(LogoutView):
    pass
