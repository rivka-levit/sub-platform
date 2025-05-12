from django.urls import path

from client import views

app_name = 'client'

urlpatterns = [
    path('dashboard/', views.ClientDashboardView.as_view(), name='dashboard'),
    path(
        'article-detail/<slug:slug>/',
        views.ArticleDetailView.as_view(),
        name='article_detail'
    ),
    path(
        'browse-articles/',
        views.BrowseArticlesView.as_view(),
        name='browse_articles'),
    path(
        'subscription-plans/',
        views.SubscriptionPlansView.as_view(),
        name='subscription_plans'
    ),
    path(
        'create-subscription/',
        views.CreateSubscriptionView.as_view(),
        name='create_subscription'),
    path(
        'delete-subscription/<str:subID>/',
        views.DeleteSubscriptionView.as_view(),
        name='delete_subscription'
    ),
    path(
        'update-subscription/<str:sub_id>/',
        views.UpdateSubscriptionView.as_view(),
        name='update_subscription'
    ),
    path(
        'paypal-subscription-confirmed/',
        views.PayPalSubConfirmedView.as_view(),
        name='paypal_subscription_confirmed'
    ),
    path(
        'django-subscription-confirmed/<str:subID>/',
        views.DjangoSubConfirmedView.as_view(),
        name='django_subscription_confirmed'
    ),
    path('deactivate-subscription/<str:sub_id>/',
         views.deactivate_subscription,
         name='deactivate_subscription'
    ),
]
