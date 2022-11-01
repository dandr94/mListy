from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from mListy.list.forms import CreateListForm


class CreateListView(LoginRequiredMixin, CreateView):
    form_class = CreateListForm
    template_name = 'list/create_list.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
