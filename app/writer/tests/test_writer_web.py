"""
Tests for writer web pages.
Command: pytest writer/tests/test_writer_web.py --cov=writer --cov-report term-missing:skip-covered
"""

import pytest

from django.contrib.messages import get_messages

from django.urls import reverse
from django.utils.text import slugify

from writer.models import Article

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'path_name,expected',
    [
        ('writer:dashboard', 200),
        ('writer:create_article', 200),
        ('writer:my_articles', 200)
    ]
)
def test_writer_get_page_success(client, user_writer, path_name, expected):
    """Test get writer pages get successfully."""

    client.force_login(user_writer)

    r = client.get(reverse(path_name, kwargs={'writer_id': user_writer.id}))

    assert r.status_code == expected


def test_writer_not_authenticated_redirect(client, user_writer):
    """Test not authenticated redirect to login page."""

    r = client.get(reverse('writer:dashboard',
                           kwargs={'writer_id': user_writer.id}))

    assert r.status_code == 302
    assert r['Location'] == (f'{reverse('login')}?redirect_to='
                             f'{reverse("writer:dashboard", 
                                        kwargs={'writer_id': user_writer.id})}')


def test_create_article_has_protected_form(client, user_writer):
    client.force_login(user_writer)

    r = client.get(reverse(
        'writer:create_article',
        kwargs={'writer_id': user_writer.id}
    ))
    assert r.status_code == 200
    assert 'article_form' in r.context
    assert 'csrf_token' in r.context


def test_create_article_form_fields_correct(client, user_writer):
    client.force_login(user_writer)
    r = client.get(reverse(
        'writer:create_article',
        kwargs={'writer_id': user_writer.id}
    ))
    page_body = str(r.content)

    assert r.status_code == 200
    assert 'for="id_title"' in page_body
    assert 'for="id_slug"' in page_body
    assert 'for="id_content"' in page_body
    assert 'type="checkbox"' in page_body
    assert 'type="submit"' in page_body


def test_create_article_post_success(client, user_writer):
    payload = {
        'title': 'Sample Article Title',
        'content': 'Sample Article Content',
    }
    client.force_login(user_writer)
    r = client.post(
        reverse('writer:create_article', kwargs={'writer_id': user_writer.id}),
        data=payload
    )
    new_article = Article.objects.filter(title=payload['title'])

    assert r.status_code == 302
    assert r['Location'] == reverse(
        'writer:my_articles',
        kwargs={'writer_id': user_writer.id}
    )
    assert new_article.exists()
    assert len(new_article) == 1
    assert new_article[0].slug == slugify(payload['title'])


def test_create_article_post_invalid_form_fails(client, user_writer):
    payload = {
        'slug': 'some-article-slug',
        'content': 'Sample article content',
    }
    client.force_login(user_writer)
    r = client.post(
        reverse('writer:create_article', kwargs={'writer_id': user_writer.id}),
        data=payload
    )
    new_article = Article.objects.filter(slug=payload['slug'])
    response_messages = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert len(response_messages) == 1
    assert response_messages[0].message == 'Something went wrong!'
    assert new_article.exists() is False


def test_my_articles_get_list_success(client, user_writer, article):
    a1 = article(user_writer, title='Article 1')
    a2 = article(user_writer, title='Article 2')

    client.force_login(user_writer)
    r = client.get(reverse(
        'writer:my_articles',
        kwargs={'writer_id': user_writer.id}
    ))
    page_body = str(r.content)

    assert r.status_code == 200
    assert 'articles' in r.context
    assert len(r.context['articles']) == 2
    assert a1.title in page_body
    assert a2.title in page_body


def test_my_articles_get_only_logged_user_articles(client, user, article):
    user1 = user(
        email='user1@example.com',
        password='test_pass123',
        is_writer=True
    )
    user2 = user(
        email='user2@example.com',
        password='test_pass123',
        is_writer=True
    )

    article(user1)
    article(user2, title='Article 1 of user2')
    article(user2, title='Article 2 of user2')

    client.force_login(user1)
    r = client.get(reverse(
        'writer:my_articles',
        kwargs={'writer_id': user1.id}
    ))
    assert 'articles' in r.context
    assert len(r.context['articles']) == 1

    client.logout()

    client.force_login(user2)
    r = client.get(reverse(
        'writer:my_articles',
        kwargs={'writer_id': user2.id}
    ))
    assert 'articles' in r.context
    assert len(r.context['articles']) == 2


def test_update_article_has_form_with_content(client, user_writer, article):
    a = article(user_writer)
    client.force_login(user_writer)
    r = client.get(reverse(
        'writer:update_article',
        kwargs={'writer_id': user_writer.id, 'slug': a.slug}
    ))
    page_body = str(r.content)

    assert r.status_code == 200
    assert 'article_form' in r.context
    assert 'csrf_token' in r.context
    assert f'value="{a.title}"' in page_body
    assert f'value="{a.slug}"' in page_body
    assert a.content in page_body


def test_update_article_success(client, user_writer, article):
    a = article(user_writer)
    client.force_login(user_writer)
    payload = {'title': 'Changed Title', 'slug': slugify('Changed Title')}

    r = client.post(
        reverse('writer:update_article',
                kwargs={'writer_id': user_writer.id, 'slug': a.slug}),
        data=payload
    )
    a.refresh_from_db()

    assert r.status_code == 302
    assert r['Location'] == reverse('writer:my_articles',
                                    kwargs={'writer_id': user_writer.id})
    assert a.title == payload['title']
    assert a.slug == payload['slug']


def test_update_article_post_invalid_form_fails(client, user_writer, article):
    a = article(user_writer)
    client.force_login(user_writer)
    payload = {'title': ''}
    r = client.post(
        reverse('writer:update_article',
                kwargs={'writer_id': user_writer.id, 'slug': a.slug}),
        data=payload
    )
    a_not_updated = Article.objects.get(id=a.id)
    response_messages = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert len(response_messages) == 1
    assert response_messages[0].level == 40
    assert response_messages[0].message == ('Article update failed! '
                                            'Invalid data has been submitted.')
    assert a.title == a_not_updated.title


def test_delete_article_success(client, user_writer, article):
    a = article(user_writer)
    client.force_login(user_writer)
    r = client.get(reverse(
        'writer:delete_article',
        kwargs={'writer_id': user_writer.id, 'slug': a.slug}
    ))
    messages_received = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert r['Location'] == reverse('writer:my_articles',
                                    kwargs={'writer_id': user_writer.id})
    query = Article.objects.filter(slug=a.slug)

    assert query.exists() is False
    assert len(messages_received) == 1
    assert messages_received[0].level == 25
    assert messages_received[0].message == 'Article deleted successfully!'

def test_delete_article_that_does_not_exist(client, user_writer):
    """Test deletion of an article that does not exist returns appropriate
    message to `My Articles` page."""

    client.force_login(user_writer)
    r = client.get(reverse(
        'writer:delete_article',
        kwargs={'writer_id': user_writer.id, 'slug': 'some-slug'}
    ))
    messages_received = list(get_messages(r.wsgi_request))

    assert r.status_code == 302
    assert r['Location'] == reverse('writer:my_articles',
                                    kwargs={'writer_id': user_writer.id})
    assert len(messages_received) == 1
    assert messages_received[0].level == 20
    assert messages_received[0].message == 'Article not found.'
