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
]
