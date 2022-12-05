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
    template_name = 'list/details_list.html'
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

        entries_dict = {x: [x.movie.duration, x.grade] for x in context['movie_list'].listentry_set.all()}

        total_time_minutes = return_minutes(entries_dict)

        stats = return_time_stats(total_time_minutes)

        context['total_time_days'] = stats[0]
        context['total_time_hours'] = stats[1]
        context['average_grade'] = return_list_average_grade(entries_dict)

        return context
