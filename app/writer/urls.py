from django.urls import path

from writer import views

app_name = 'writer'

urlpatterns = [
    path(
        '<int:writer_id>/dashboard/',
        views.WriterDashboardView.as_view(),
        name='dashboard'
    ),
    path(
        '<int:writer_id>/create-article/',
        views.CreateArticleView.as_view(),
        name='create_article'
    ),
    path(
        '<int:writer_id>/my-articles/',
        views.MyArticlesView.as_view(),
        name='my_articles'
    ),
    path(
        '<int:writer_id>/update-article/<slug:slug>/',
        views.UpdateArticleView.as_view(),
        name='update_article'
    ),
    path(
        '<int:writer_id>/delete-article/<slug:slug>/',
        views.delete_article,
        name='delete_article'
    ),
]
