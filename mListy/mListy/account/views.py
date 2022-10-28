from django.views.generic import TemplateView


class HomeViewNoProfile(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # FIX NOT NECESSARY
        return context
