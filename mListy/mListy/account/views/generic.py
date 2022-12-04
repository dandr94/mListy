from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from mListy.list.models import List


class HomeViewNoProfile(TemplateView):
    template_name = 'home/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'home/dashboard.html'
    context_object_name = 'lists'

    def get_queryset(self):
        queryset = List.objects.filter(user=self.request.user).order_by('date_created')
        return queryset


class About(TemplateView):
    template_name = 'about.html'
