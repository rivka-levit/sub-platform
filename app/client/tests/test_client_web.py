"""
Tests for client web pages.
Command: pytest client/tests/test_client_web.py --cov=client --cov-report term-missing:skip-covered
"""

import pytest

from django.shortcuts import reverse
from django.contrib.messages import get_messages

from unittest.mock import patch, MagicMock

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
