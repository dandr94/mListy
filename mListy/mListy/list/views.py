from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from mListy.account.mixins import PermissionHandlerMixin
from mListy.list.forms import CreateListForm, EditListForm
from mListy.list.models import List


class CreateListView(LoginRequiredMixin, CreateView):
    form_class = CreateListForm
    template_name = 'list/create_list.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditListView(LoginRequiredMixin, PermissionHandlerMixin, UpdateView):
    model = List
    template_name = 'list/edit_list.html'
    form_class = EditListForm
    success_url = reverse_lazy('dashboard')

