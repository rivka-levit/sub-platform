from django.urls import path

from writer import views

app_name = 'writer'

urlpatterns = [
    path(
        '<int:writer_id>/dashboard/',
        views.WriterDashboardView.as_view(),
        name='dashboard'
    ),
]
