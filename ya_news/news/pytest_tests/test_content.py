import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, home_url):
    """Проверка количества новостей на главной странице."""
    assert client.get(home_url).context['object_list'].count(
    ) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url):
    """Проверка сортировки новостей от новых к старым."""
    all_dates = [
        news_item.date for news_item in client.get(
            home_url).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, detail_url):
    """Проверка сортировки комментариев от старых к новым."""
    assert 'news' in client.get(detail_url).context
    comments_dates = client.get(
        detail_url).context['news'].comment_set.values_list(
        'created', flat=True)
    assert list(comments_dates) == sorted(comments_dates)


def test_anonymous_client_has_no_form(client, detail_url):
    """Проверка отсутствия формы комментария для анонима."""
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(author_client, detail_url):
    """Проверка наличия формы комментария для авторизованного."""
    assert isinstance(author_client.get(
        detail_url).context.get('form'), CommentForm)
