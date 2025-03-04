from django.views.generic import TemplateView, View

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.shortcuts import redirect, reverse, render

from writer.forms import ArticleForm


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


class CreateArticleView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request, writer_id):  # noqa
        form = ArticleForm()
        context = {
            'article_form': form,
            'title': 'Edenthought | Create Article'
        }

        return render(request, 'writer/create_article.html', context=context)


    def post(self, request, writer_id):  # noqa
        user = get_user_model().objects.get(id=self.request.user.id)
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = user
            article.save()
            messages.success(request, 'Article created successfully!')
            return redirect(reverse('writer:my_articles', kwargs={'writer_id': writer_id}))

        messages.error(request, 'Something went wrong!')
        return redirect(request.META.get(
                        'HTTP_REFERER',
                        reverse('writer:my_articles',
                                kwargs={'writer_id': self.request.user.id}))
        )
