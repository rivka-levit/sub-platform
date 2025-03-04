from django.urls import path

from account import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('delete-account', views.delete_account, name='delete_account'),
]