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
]
