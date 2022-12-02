from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from mListy.account.forms import EditProfileForm, ChangePasswordForm
from mListy.account.mixins import PermissionHandlerMixin
from mListy.account.models import Profile
from mListy.list.models import List
from mListy.account.helpers import return_last_added_entries, return_total_average_grade


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'account/details_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user_id == self.request.user.id
        context['user_lists'] = List.objects \
            .prefetch_related('listentry_set__movie') \
            .filter(user_id=self.object.user_id)
        entries_dict = {x: x.grade for i in context['user_lists'] for x in i.listentry_set.all()}
        context['total_movies'] = len(entries_dict)
        context['total_average_grade'] = return_total_average_grade(entries_dict)
        context['last_added'] = return_last_added_entries(entries_dict)
        return context


class EditProfileView(LoginRequiredMixin, PermissionHandlerMixin, UpdateView):
    model = Profile
    template_name = 'account/edit_profile.html'
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('details profile', kwargs={'slug': self.object.slug})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('dashboard')
