from django.contrib import admin

from client.models import SubscriptionPlan, Subscription

admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
