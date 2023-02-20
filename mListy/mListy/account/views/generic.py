from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from mListy.account.helpers import return_trending_movies
from mListy.list.models import List


class HomeViewNoProfile(TemplateView):
    template_name = 'home/index/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'home/dashboard/dashboard.html'
    context_object_name = 'lists'

    def get_queryset(self):
        queryset = List.objects.filter(user=self.request.user).order_by('date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['trending'] = return_trending_movies()

        return context


class About(TemplateView):
    template_name = 'about/about.html'
