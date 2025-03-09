"""
Test models of client app.
Command: pytest client/tests/test_client_models.py --cov=client --cov-report=term-missing:skip-covered
"""

import pytest

from client.models import Subscription, SubscriptionPlan

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('plan_name,plan_cost',
                         [('standard', 4.99), ('premium', 9.99)])
def test_create_subscription_plan_success(plan_name, plan_cost):
    """Test creating a subscription plan successfully."""

    data = {
        'name': plan_name,
        'cost': plan_cost,
        'description': 'Sample plan description'
    }

    plan = SubscriptionPlan.objects.create(**data)

    for k, v in data.items():
        assert getattr(plan, k) == v

    assert str(plan) == plan_name


def test_create_standard_subscription_success(sample_user, standard):
    """Test create standard subscription with default parameters."""

    data = {
        'subscriber_name': f'{sample_user.first_name}_{sample_user.last_name}',
        'subscription_plan': standard,
        'paypal_subscription_id': 'aui6rb2sd8iu45y8gf0',
        'user': sample_user
    }

    subscription = Subscription.objects.create(**data)

    for k, v in data.items():
        assert getattr(subscription, k) == v

    assert subscription.is_active == False
    assert subscription.subscription_plan.cost == standard.cost
    assert str(subscription) == (
        f'{subscription.subscriber_name} - '
        f'{subscription.subscription_plan.name.capitalize()} subscription'
    )


def test_create_premium_subscription_active_success(sample_user, premium):
    """Test create active premium subscription successfully."""

    data = {
        'subscriber_name': f'{sample_user.first_name}_{sample_user.last_name}',
        'paypal_subscription_id': 'aui6rb2sd8iu45y8gf0',
        'user': sample_user,
        'is_active': True,
        'subscription_plan': premium
    }

    subscription = Subscription.objects.create(**data)

    assert subscription.subscription_plan == premium
    assert subscription.subscription_plan.cost == premium.cost
    assert subscription.is_active == True
