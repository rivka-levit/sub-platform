from django.urls import path

from client import views

app_name = 'client'

urlpatterns = [
path('dashboard/', views.ClientDashboardView.as_view(), name='dashboard'),
]