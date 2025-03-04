from django.views.generic import TemplateView, View, ListView

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.shortcuts import redirect, reverse, render, get_object_or_404

from writer.forms import ArticleForm
from writer.models import Article


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


class MyArticlesView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Article
    template_name = 'writer/my_articles.html'
    context_object_name = 'articles'

    def dispatch(self, request, *args, **kwargs):
        return super(MyArticlesView, self).dispatch(
            request,
            self.kwargs['writer_id'],
            *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edenthought | My Articles'
        return context

    def get_queryset(self):
        return (super().get_queryset().filter(author=self.request.user)
                .order_by('-date_posted'))


class UpdateArticleView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request, writer_id, slug):  # noqa
        user = get_object_or_404(get_user_model(), id=self.request.user.id)
        article = get_object_or_404(Article, slug=slug, author=user)
        form = ArticleForm(instance=article)
        context = {
            'article_form': form,
            'title': 'Edenthought | Update Article',
            'article': article
        }
        return render(request, 'writer/update_article.html', context=context)

    def post(self, request, writer_id, slug):  # noqa
        user = get_object_or_404(get_user_model(), id=self.request.user.id)
        article = get_object_or_404(Article, slug=slug, author=user)
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect(reverse('writer:my_articles',
                                    kwargs={'writer_id': self.request.user.id}))

        messages.error(request, 'Article update failed! Invalid data has been submitted.')
        return redirect(request.META.get(
            'HTTP_REFERER',
            reverse('writer:my_articles',
            kwargs={'writer_id': self.request.user.id}))
        )


@login_required(redirect_field_name='redirect_to', login_url='login')
def delete_article(request, writer_id, slug):
    user = get_object_or_404(get_user_model(), id=request.user.id)
    try:
        article = Article.objects.get(slug=slug, author=user)
        article.delete()
        messages.success(request, 'Article deleted successfully!')
    except Article.DoesNotExist:
        messages.info(request, 'Article not found.')

    return redirect(reverse('writer:my_articles',
                            kwargs={'writer_id': request.user.id}))
