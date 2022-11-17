from django.views.generic import DetailView

from mListy.account.models import Profile
from mListy.list.models import List, ListEntry
from mListy.movie.helpers import return_list_with_additional_stats


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'account/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user_id == self.request.user.id
        context['user_lists'] = List.objects.filter(user_id=self.object.user_id)
        context['entries'] = ListEntry.objects.filter(list__user_id=self.object.user.id)
        context['total_average_grade'] = sum([e.grade for e in context['entries']]) // len(context['entries'])
        context['user_lists_dict'] = return_list_with_additional_stats(context['user_lists'], context['entries'])

        return context
