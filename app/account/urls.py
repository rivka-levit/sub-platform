from django.urls import path
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('delete-account', views.delete_account, name='delete_account'),

    # Password management

    # Enter email to receive password reset link
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(),
        name='reset_password'
    ),

    # Email sent successfully page
    path(
        'reset-password/sent/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    # Change password link
    path(
        'reset-password/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    # Success page password has been changed
    path(
        'reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]
