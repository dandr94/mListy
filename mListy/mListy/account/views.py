from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView

from mListy.account.forms import CreateUserForm, LoginAccountForm
from mListy.account.models import Profile


class HomeViewNoProfile(TemplateView):
    template_name = 'index.html'


class RegisterUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class LoginUserView(LoginView):
    form_class = LoginAccountForm
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


class LogoutUserView(LogoutView):
    pass


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'account/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user_id == self.request.user.id
        return context
