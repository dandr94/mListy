from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from mListy.account.mixins import PermissionHandlerMixin
from mListy.list.forms import CreateListForm, EditListForm, DeleteListForm
from mListy.list.helpers import return_time_stats, return_minutes, return_list_average_grade, sort_entries_by_grade_name
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


class DeleteListView(LoginRequiredMixin, PermissionHandlerMixin, DeleteView):
    template_name = 'list/delete_list.html'
    form_class = DeleteListForm
    model = List
    success_url = reverse_lazy('dashboard')


class DetailsListView(ListView):
    model = List
    template_name = 'list/details/details_list.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        try:
            queryset = List.objects.prefetch_related('listentry_set__movie').get(slug=self.kwargs['slug'])
        except List.DoesNotExist:
            raise Http404

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = context['object_list'].user.id == self.request.user.id

        context['entries'] = sort_entries_by_grade_name(context['movie_list'].listentry_set.all())

        # Total time here is not calculated only for Completed because maybe you can have a list
        # that is only for planned movies, and you want to see how much time you will need to spend
        # to watch them all. For that reason maybe change the text to something more clear.

        total_time_minutes = return_minutes(context['entries'])

        days, hours, minutes = return_time_stats(total_time_minutes)

        context['total_time_days'] = days
        context['total_time_hours'] = hours
        context['total_time_minutes'] = minutes

        context['average_grade'] = return_list_average_grade(context['entries'])

        return context
