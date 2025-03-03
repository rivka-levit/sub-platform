from django.views.generic import TemplateView

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import redirect


class WriterDashboardView(TemplateView):
    template_name = 'writer/writer_dashboard.html'

    @method_decorator(login_required(
        login_url='login',
        redirect_field_name='redirect_to'
    ))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_writer:  # noqa
            return super(WriterDashboardView, self).dispatch(
                request,
                request.user.id,
                *args, **kwargs
            )

        return redirect('client:dashboard')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | Writer Dashboard'
        return context