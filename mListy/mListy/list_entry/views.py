from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from mListy.account.mixins import EntryPermissionHandlerMixin
from mListy.list.models import List
from mListy.list_entry.forms import AddListEntryForm, EditListEntryForm, DeleteListEntryForm
from mListy.list_entry.models import ListEntry
from mListy.movie.models import MovieDB


class AddListEntryView(LoginRequiredMixin, CreateView):
    template_name = 'list_entry/add_entry.html'
    form_class = AddListEntryForm
    context_object_name = 'entry'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['user_lists'] = List.objects.filter(user_id=self.request.user.id)
        kwargs['movie'] = MovieDB.objects.get(slug=self.kwargs['slug'])

        return kwargs

    def get_success_url(self):
        return reverse_lazy('details movie', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_slug'] = self.kwargs['slug']
        context['movie_name'] = context['form'].movie
        return context


class EditListEntryView(LoginRequiredMixin, EntryPermissionHandlerMixin, UpdateView):
    model = ListEntry
    template_name = 'list_entry/edit_entry.html'
    form_class = EditListEntryForm
    context_object_name = 'entry'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_lists'] = List.objects.filter(user_id=self.request.user.id)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('details list', kwargs={'slug': self.object.list.slug})


class DeleteListEntryView(LoginRequiredMixin, EntryPermissionHandlerMixin, DeleteView):
    model = ListEntry
    template_name = 'list_entry/delete_entry.html'
    context_object_name = 'entry'
    form_class = DeleteListEntryForm

    def get_success_url(self):
        return reverse_lazy('details list', kwargs={'slug': self.object.list.slug})
