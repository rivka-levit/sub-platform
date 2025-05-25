"""
Tests for client web pages.
Command: pytest client/tests/test_client_web.py --cov=client --cov-report term-missing:skip-covered
"""

import pytest

from django.shortcuts import reverse
from django.contrib.messages import get_messages

from unittest.mock import patch, MagicMock

from django.template.defaultfilters import title

from client.models import Subscription

pytestmark = pytest.mark.django_db


def test_get_dashboard(client, sample_user):
    """Test get method dashboard returns correct page."""

    client.force_login(sample_user)
    r = client.get(reverse('client:dashboard'))
    page_content = r.content.decode('utf-8')

    assert r.status_code == 200
    assert f'Welcome, {sample_user.first_name}!' in page_content


def test_get_dashboard_not_authenticated_redirect(client):
    """Test non-authenticated user is redirected to login page."""

    r = client.get(reverse('client:dashboard'))

    assert r.status_code == 302
    assert r['Location'] == (f'{reverse('login')}?redirect_to='
                             f'{reverse("client:dashboard")}')


def test_get_dashboard_writer_redirect_to_writer_dashboard(client, user_writer):
    """Test writer get client dashboard receives writer dashboard page."""

    client.force_login(user_writer)
    r = client.get(reverse('client:dashboard'))

    assert r.status_code == 302
    assert r['Location'] == reverse('writer:dashboard',
                                    kwargs={'writer_id': user_writer.id})


def test_article_detail_get_success(client, sample_user, user_writer, article):

    payload = {'title': 'Sample Article'}
    a = article(user_writer, **payload)

    client.force_login(sample_user)
    r = client.get(reverse('client:article_detail', kwargs={'slug': a.slug}))

    page_content = r.content.decode('utf-8')

    assert r.status_code == 200
    assert payload['title'] in r.context['title']
    assert payload['title'] in page_content
    assert a.content in page_content


def test_sub_plans_page_renders_correct_template(client, sample_user):
    """Test subscription plan page renders correct template with
    the information about subscription plans."""

    client.force_login(sample_user)
    r = client.get(reverse('client:subscription_plans'))
    page_content = r.content.decode('utf-8')

    assert r.status_code == 200
    assert 'Standard subscription' in page_content
    assert 'Premium subscription' in page_content
    assert 'id="paypal-button-container-P-9EN41519BU401782AM7HQXXI"' in page_content
    assert 'id="paypal-button-container-P-2JB54269VP863135RM7HQZFY"' in page_content


@pytest.mark.parametrize(
    'sub_plan,output_expected',
    [('standard', 'Standard'), ('premium', 'Premium')]
)
def test_sub_plan_output_on_client_dashboard(
        sub_plan, output_expected, client, sample_user, subscription, request
):
    """Test subscription plan output on client dashboard successfully."""

    subscription(user=sample_user, plan=request.getfixturevalue(sub_plan))

    client.force_login(sample_user)
    r = client.get(reverse('client:dashboard'))
    body = r.content.decode('utf-8')

    assert r.status_code == 200
    assert 'sub_plan' in r.context
    assert output_expected in body


def test_none_sub_plan_output_none(client, sample_user):
    """Test client dashboard without subscription None subscription plan."""

    client.force_login(sample_user)
    r = client.get(reverse('client:dashboard'))
    body = r.content.decode('utf-8')

    assert r.status_code == 200
    assert 'sub_plan' not in r.context
    assert 'None' in body


@pytest.mark.parametrize('sub_plan', ['standard', 'premium'])
def test_create_subscription_success(
        sub_plan, client, sample_user, request
):
    """Test creating subscription via web page successfully."""

    sub_id = 'I-FF857850J03'
    plan = request.getfixturevalue(sub_plan)

    client.force_login(sample_user)
    r = client.get('%s?subID=%s&plan=%s' % (reverse('client:create_subscription'), sub_id, plan.name))
    sbn = Subscription.objects.filter(user=sample_user, subscription_plan=plan)

    assert r.status_code == 302
    assert r['Location'] == reverse('client:dashboard')
    assert sbn.exists()
    assert len(sbn) == 1


def test_duplicated_create_subscription_fails(client, sample_user, standard, premium, subscription):
    """Test creating duplicated subscription fails."""

    subscription(user=sample_user, plan=standard)
    sub_id = 'I-FF84TRR0J08'

    client.force_login(sample_user)
    r = client.get('%s?subID=%s&plan=%s' % (reverse('client:create_subscription'),
                                            sub_id,
                                            premium.name))
    message_received = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert len(message_received) == 1
    assert message_received[0].level == 40
    assert 'Subscription not created!' in message_received[0].message


def test_delete_subscription_view_renders_correct_template(
        client,
        sample_user,
        subscription,
        standard
):
    """Test delete subscription view renders correct template
    when subscription is not deleted."""

    sbn = subscription(user=sample_user, plan=standard)
    client.force_login(sample_user)

    r = client.get(reverse(
        'client:delete_subscription',
        kwargs={'subID': sbn.paypal_subscription_id})
    )

    assert r.status_code == 200
    assert 'Delete Subscription' in r.context['title']
    assert 'is_deleted' in r.context
    assert r.context['is_deleted'] is False
    assert 'Something went wrong!' in r.content.decode('utf-8')


@patch('client.views.cancel_subscription_paypal')
def test_delete_subscription_success(
        mocked_paypal,
        client,
        sample_user,
        subscription,
        standard
):
    """Test delete subscription successfully."""

    sbn = subscription(user=sample_user, plan=standard)
    client.force_login(sample_user)
    mocked_paypal.return_value = True

    r = client.get(reverse(
        'client:delete_subscription',
        kwargs={'subID': sbn.paypal_subscription_id})
    )

    assert r.status_code == 200
    assert r.context['is_deleted'] == True

    subscriptions = Subscription.objects.filter(user=sample_user)

    assert subscriptions.exists() == False


@pytest.mark.parametrize(
    'sub_plan,articles_qty',
    [('standard', 1), ('premium', 2)]
)
def test_browse_articles_standard_success(
        sub_plan, articles_qty, client, sample_user, user_writer, article,
        subscription, request
):
    """Test browse articles retrieves standard articles for standard subscription."""

    plan = request.getfixturevalue(sub_plan)
    subscription(user=sample_user, plan=plan)
    article(user_writer)
    article(user_writer, title='Premium Article', is_premium=True)
    client.force_login(sample_user)

    r = client.get(reverse('client:browse_articles'))

    assert r.status_code == 200
    assert 'articles' in r.context
    assert len(r.context['articles']) == articles_qty


def test_browse_no_articles_without_subscription(
        client, sample_user, user_writer, article
):
    """Test browse articles retrieves no articles for user without subscription."""

    article(user_writer)
    client.force_login(sample_user)

    r = client.get(reverse('client:browse_articles'))

    assert r.status_code == 200
    assert 'articles' in r.context
    assert r.context['articles'] is None
