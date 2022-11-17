from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from mListy.account.mixins import PermissionHandlerMixin
from mListy.list.forms import CreateListForm, EditListForm, DeleteListForm
from mListy.list.models import List, ListEntry


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


class DeleteListView(DeleteView):
    template_name = 'list/delete_list.html'
    form_class = DeleteListForm
    model = List
    success_url = reverse_lazy('dashboard')


class DetailsListView(ListView):
    model = ListEntry
    template_name = 'list/list_details.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        queryset = ListEntry.objects.filter(list__slug=self.kwargs['slug']).order_by('-grade')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_time_minutes'] = sum([movie.movie.duration for movie in context['movie_list']])
        context['total_time_hours'] = context['total_time_minutes'] / 60
        context['total_time_days'] = context['total_time_hours'] / 24
        context['average_grade'] = sum([movie.grade for movie in context['movie_list']]) // len(context['movie_list'])
        return context
