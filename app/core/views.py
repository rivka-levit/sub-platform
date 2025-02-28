from django.views.generic import TemplateView, View


class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = {'title': 'Edenthought'}
        return context
