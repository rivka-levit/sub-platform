"""
Tests for writer app models.
Command: pytest writer/tests/test_writer_models.py --cov=writer --cov-report term-missing:skip-covered
"""

import pytest

from django.utils.text import slugify
from django.db.utils import IntegrityError

from writer.models import Article

pytestmark = pytest.mark.django_db


def test_create_article_pass(user_writer):
    """Test creating an article successfully."""

    data = {
        'title': 'Test title',
        'content': 'Test content',
        'author': user_writer,
    }

    article = Article.objects.create(**data)

    assert article.title == data['title']
    assert article.content == data['content']
    assert article.author == user_writer
    assert article.slug == slugify(data['title'])
    assert str(article) == article.title


def test_create_article_with_repeating_slug_same_user_fails(user_writer):
    """Test creating an article of the same user with repeating slug fails."""

    data = {
        'title': 'Test title',
        'content': 'Test content',
        'author': user_writer,
    }

    Article.objects.create(**data)

    with pytest.raises(IntegrityError):
        Article.objects.create(**data)

def test_create_article_with_repeating_slug_different_users_pass(user):
    """Test creating an article with the same slug to different users pass."""

    writer1 = user(email='writer1@example.com', is_writer=True)
    writer2 = user(email='writer2@example.com', is_writer=True)

    payload1 = {'title': 'Test title 1', 'slug': 'repeating-slug',
                'content': 'Test content 1', 'author': writer1}
    payload2 = {'title': 'Test title 2', 'slug': 'repeating-slug',
                'content': 'Test content 2', 'author': writer2}

    Article.objects.create(**payload1)
    Article.objects.create(**payload2)

    query_set = Article.objects.filter(slug='repeating-slug')

    assert query_set.count() == 2

def test_create_article_with_custom_slug_success(user_writer):
    """Test creating an article with custom slug successfully."""

    data = {
        'title': 'Test title',
        'content': 'Test content',
        'slug': 'custom-title-slug',
        'author': user_writer,
    }

    article = Article.objects.create(**data)
    assert article.title == data['title']
    assert article.slug == data['slug']
