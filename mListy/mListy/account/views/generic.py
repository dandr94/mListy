from django.views.generic import TemplateView, ListView


class HomeViewNoProfile(TemplateView):
    template_name = 'index.html'


class Dashboard(ListView):
    template_name = 'dashboard.html'