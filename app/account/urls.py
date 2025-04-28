"""
URL configuration for account app.
"""

from django.urls import path
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('delete-account', views.delete_account, name='delete_account'),

    # ----------- Password management --------------

    # Enter email to receive password reset link
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(template_name='account/password_reset.html',),
        name='reset_password'
    ),

    # Email sent success page
    path(
        'reset-password/sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
        name='password_reset_done'
    ),

    # Change password form link
    path(
        'reset-password/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'),
        name='password_reset_confirm'
    ),

    # Success page password has been changed
    path(
        'reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    # ------------- Email verification ----------------

    path(
        'email-verification/',
        views.EmailVerificationView.as_view(),
        name='email_verification'
    ),
    path(
        'email-verification-sent/',
        views.EmailVerificationSentView.as_view(),
        name='email_verification_sent'
    ),
    path(
        'email-verification-success/',
        views.EmailVerificationSuccessView.as_view(),
        name='email_verification_success'
    ),
    path(
        'email-verification-failed/',
        views.EmailVerificationFailedView.as_view(),
        name='email_verification_failed'
    ),
]
