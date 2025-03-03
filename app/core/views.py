from django.views.generic import TemplateView, View

from django.shortcuts import redirect, reverse


class HomeView(TemplateView):
    template_name = 'core/index.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            if user.is_writer:  # noqa
                return redirect(reverse(
                    'writer:dashboard',
                    kwargs={'writer_id': user.id}
                ))
            return redirect(reverse('client:dashboard'))

        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {'title': 'Edenthought'}
        return context
