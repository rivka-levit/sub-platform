from django.db import models

from django.contrib.auth import get_user_model


class SubscriptionPlan(models.Model):
    paypal_plan_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    cost = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'subscription plan'
        verbose_name_plural = 'subscription plans'

    def __str__(self):
        return f'{self.name}'


class Subscription(models.Model):
    subscriber_name = models.CharField(max_length=255)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name='subscription_plan'
    )
    paypal_subscription_id = models.CharField(max_length=300)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscription',
        max_length=10,
        unique=True
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return (f'{self.subscriber_name} - '
                f'{self.subscription_plan.name.capitalize()} subscription')
