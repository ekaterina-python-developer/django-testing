from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND
FOUND = HTTPStatus.FOUND

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client, method, expected_status',
    [
        # Публичные GET-страницы
        (lf('home_url'), lf('anonymous_client'), 'get', OK),
        (lf('detail_url'), lf('anonymous_client'), 'get', OK),
        (lf('login_url'), lf('anonymous_client'), 'get', OK),
        (lf('signup_url'), lf('anonymous_client'), 'get', OK),

        # POST-запрос на logout
        (lf('logout_url'), lf('anonymous_client'), 'post', OK),

        # Приватные страницы для автора
        (lf('edit_url'), lf('author_client'), 'get', OK),
        (lf('delete_url'), lf('author_client'), 'get', OK),

        # Запрещённые страницы для читателя
        (lf('edit_url'), lf('reader_client'), 'get', NOT_FOUND),
        (lf('delete_url'), lf('reader_client'), 'get', NOT_FOUND),

        # Редиректы для анонимов
        (lf('edit_url'), lf('anonymous_client'), 'get', FOUND),
        (lf('delete_url'), lf('anonymous_client'), 'get', FOUND),
    ]
)
def test_status_codes(url, client, method, expected_status):
    """Проверка кодов состояния для всех маршрутов."""
    response = getattr(client, method)(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_url',
    [
        (lf('edit_url'), lf('edit_redirect_url')),
        (lf('delete_url'), lf('delete_redirect_url')),
    ]
)
def test_anonymous_redirects(url, redirect_url, anonymous_client):
    """Проверка редиректов для неавторизованных пользователей."""
    response = anonymous_client.get(url)
    assertRedirects(response, redirect_url)
