from django.shortcuts import redirect, reverse

from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


class ClientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'client/client_dashboard.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_writer:  # noqa
            return redirect(reverse(
                'writer:dashboard',
                kwargs={'writer_id': request.user.id}
            ))

        return super(ClientDashboardView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # subscriptions = Subscription.objects.filter(
        #     user=self.request.user,
        #     is_active=True
        # ).order_by('-id')
        #
        # if subscriptions.exists():
        #     context['sub_plan'] = subscriptions[0].subscription_plan

        context['title'] = 'Edenthought | Dashboard'

        return context
