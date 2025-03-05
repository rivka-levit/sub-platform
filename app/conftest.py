import pytest

from django.contrib.auth import get_user_model

from account.models import CustomUser

from writer.models import Article
# from client.models import Subscription, SubscriptionPlan


@pytest.fixture
def sample_user() -> CustomUser:
    return CustomUser.objects.create_user(
        email='sample_user@example.com',
        password='sample_password123',
        first_name='Sample First Name',
        last_name='Sample Last Name'
    )


@pytest.fixture
def user_writer() -> CustomUser:
    return CustomUser.objects.create_user(
        email='writer@example.com',
        password='writer_password123',
        first_name='Writer First Name',
        last_name='Writer Last Name',
        is_writer=True
    )


@pytest.fixture
def superuser() -> CustomUser:
    return CustomUser.objects.create_superuser(
        email='superuser@example.com',
        password='test_password123',
        first_name='Superuser First Name',
        last_name='Superuser Last Name'
    )


@pytest.fixture
def user():
    """Fixture for creating a sample user and pass other parameters."""

    payload = {
        'email': 'user@example.com',
        'password': 'test_pass123',
        'first_name': 'Sample First Name',
        'last_name': 'Sample Last Name'
    }

    def _user_factory(**kwargs):
        if kwargs:
            payload.update(kwargs)

        return CustomUser.objects.create_user(**payload)

    return _user_factory


@pytest.fixture
def article():
    """Fixture for creating a sample article and pass other parameters."""

    payload = {
        'title': 'Sample Title of Sample Article',
        'content': 'Sample content',
    }

    def _article_factory(writer, **kwargs):
        payload['author'] = writer
        if kwargs:
            payload.update(kwargs)

        return Article.objects.create(**payload)

    return _article_factory


# @pytest.fixture
# def subscription():
#     """Fixture to create a sample subscription and pass other parameters."""
#
#     data = {
#         'subscriber_name': 'Sample Subscriber Name',
#         'paypal_subscription_id': 'sdf48ds0fbv3',
#         'is_active': True,
#     }
#
#     def _subscription_factory(
#             user: get_user_model(),
#             plan: SubscriptionPlan,
#             **kwargs
#     ):
#         if kwargs:
#             data.update(kwargs)
#
#         return Subscription.objects.create(user=user, subscription_plan=plan, **data)
#
#     return _subscription_factory
#
#
# @pytest.fixture
# def standard():
#     """Create standard subscription plan."""
#
#     data = {
#         'name': 'standard',
#         'cost': 4.90,
#         'description': 'Limited access'
#     }
#
#     return SubscriptionPlan.objects.create(**data)
#
#
# @pytest.fixture
# def premium():
#     """Create premium subscription plan."""
#
#     data = {
#         'name': 'premium',
#         'cost': 9.90,
#         'description': 'Full access'
#     }
#
#     return SubscriptionPlan.objects.create(**data)
