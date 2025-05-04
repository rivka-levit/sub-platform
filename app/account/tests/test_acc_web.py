"""
Tests for account web pages.
Command: pytest account/tests --cov=account --cov-report term-missing:skip-covered
"""

import pytest

from django.shortcuts import reverse

from django.contrib.auth import get_user, get_user_model
from django.contrib.messages import get_messages

from account.forms import CreateUserForm

from unittest.mock import patch, MagicMock

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, expected',
    [('index', 200), ('register', 200), ('login', 200)]
)
def test_get_page_success(url_name, expected, client):
    r = client.get(reverse(url_name))

    assert r.status_code == expected


def test_home_page_redirect_to_writer_dashboard(client, user_writer):
    """Test home page redirects logged writer to his dashboard."""

    client.force_login(user_writer)
    r = client.get(reverse('index'))

    assert r.status_code == 302
    assert r['Location'] == reverse('writer:dashboard',
                                    kwargs={'writer_id': user_writer.id})

def test_register_get_page_has_form(client):
    """Test register page contains form and it is CreateUserForm instance."""

    r = client.get(reverse('register'))
    form = r.context['register_form']

    assert 'register_form' in r.context
    assert isinstance(form, CreateUserForm)


def test_register_get_page_csrf(client):
    """Test register page contains csrf token."""

    r = client.get(reverse('register'))
    assert 'csrf_token' in r.context


def test_register_get_page_form_fields(client):
    """Test register page contains right form fields."""

    r = client.get(reverse('register'))
    page_body = str(r.content)

    assert 'type="email"' in page_body
    assert page_body.count('type="password"') == 2
    assert 'type="checkbox"' in page_body


def test_register_post_create_user_success(client):
    """Test post request with valid data creates a new user."""

    payload = {
        'email': 'new_user@example.com',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'password1': 'test_pass123',
        'password2': 'test_pass123'
    }

    r = client.post(reverse('register'), data=payload)
    new_user = get_user_model().objects.filter(email=payload['email'])

    assert r.status_code == 302
    assert new_user.exists()
    assert new_user[0].is_active == False


def test_register_post_invalid_fields_not_create_user(client):
    """Test post request with invalid data not create a new user."""

    payload = {
        'email': 'new_user@example.com',
        'first_name': 'First Name',
        'last_name': 'Last Name'
    }
    r = client.post(reverse('register'), data=payload)
    new_user = get_user_model().objects.filter(email=payload['email'])
    messages_received = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert r['Location'] == reverse('register')
    assert len(messages_received) == 1
    assert messages_received[0].level == 40
    assert 'Invalid data has been provided:' in messages_received[0].message
    assert new_user.exists() is False


def test_login_get_render_correct_form(client):
    """Test login page renders correct form."""

    r = client.get(reverse('login'))
    page_body = str(r.content)

    assert 'login_form' in r.context
    assert 'csrf_token' in r.context
    assert 'name="username"' in page_body
    assert 'name="password"' in page_body


def test_login_post_ordinary_client(client, sample_user):
    """Test ordinary client logged in."""

    r = client.post(
        reverse('login'),
        data={'username': sample_user.email, 'password': 'sample_password123'}
    )

    assert r.status_code == 302
    assert r['Location'] == reverse('client:dashboard')
    assert get_user(client) == sample_user


def test_login_post_writer(client, user_writer):
    """Test writer logged in."""

    r = client.post(
        reverse('login'),
        data={'username': user_writer.email, 'password': 'writer_password123'}
    )

    assert r.status_code == 302
    assert r['Location'] == reverse(
        'writer:dashboard',
        kwargs={'writer_id': user_writer.id}
    )
    assert get_user(client) == user_writer


def test_login_with_invalid_data_fails(client):
    """Test login with invalid data fails."""

    r = client.post(
        reverse('login'),
        data={'username': 'some@example.com', 'password': 'some_pass_123'}
    )
    messages_received = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert r['Location'] == reverse('login')
    assert len(messages_received) == 1
    assert messages_received[0].level == 40
    assert messages_received[0].message == 'Invalid username or password!'


def test_logout_success(client, sample_user):
    """Test logout successfully."""

    client.force_login(sample_user)
    r = client.get(reverse('logout'))
    messages_received = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert r['Location'] == reverse('index')
    assert get_user(client).is_anonymous
    assert len(messages_received) == 1
    assert messages_received[0].level == 25
    assert messages_received[0].message == 'You have been logged out!'


def test_update_account_get_correct_form(client, user_writer):
    """Test update account get method provides correct form."""

    client.force_login(user_writer)
    r = client.get(reverse('account'))
    page_body = str(r.content)

    assert r.status_code == 200
    assert 'csrf_token' in r.context
    assert 'id="div_id_email"' in page_body
    assert 'id="div_id_first_name"' in page_body
    assert 'id="div_id_last_name"' in page_body
    assert 'value="Update account"' in page_body


def test_update_account_post_change_data(client, user_writer):
    """Test update account successfully for writer."""

    payload = {
        'email': 'new_email@example.com',
        'first_name': 'new_first_name',
        'last_name': 'new_last_name'
    }

    client.force_login(user_writer)
    r = client.post(
        reverse('account'),
        data=payload
    )

    assert r.status_code == 302
    assert r['Location'] == reverse('index')
    assert get_user(client) == user_writer

    user_writer.refresh_from_db()

    for k, v in payload.items():
        assert getattr(user_writer, k) == v

    messages_received = list(get_messages(r.wsgi_request))

    assert len(messages_received) == 1
    assert messages_received[0].level == 25
    assert messages_received[0].message == ('Account has been updated '
                                            'successfully!')


def test_update_account_post_invalid_data_fails(client, user_writer):
    """Test update account post method fails with invalid data."""

    payload = {'email': ''}

    client.force_login(user_writer)
    r = client.post(reverse('account'), data=payload)
    messages_received = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert len(messages_received) == 1
    assert messages_received[0].level == 40
    assert 'Invalid data has been provided:' in messages_received[0].message
