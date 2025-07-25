from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_FORM_DATA = {'text': 'Тестовый текст комментария'}
BAD_WORDS_FORM_DATA = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, detail_url):
    """Проверка, что аноним не может создать комментарий."""
    client.post(detail_url, data=COMMENT_FORM_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author_client, news, author, detail_url, url_to_comments
):
    """Проверка создания комментария авторизованным пользователем."""
    response = author_client.post(detail_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    """Проверка валидации запрещенных слов в комментариях."""
    response = author_client.post(detail_url, data=BAD_WORDS_FORM_DATA)
    assert 'form' in response.context
    assert WARNING in response.context['form'].errors['text']
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, delete_url, url_to_comments):
    """Проверка удаления комментария автором."""
    response = author_client.post(delete_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
        reader_client,
        comment,
        delete_url
):
    """Проверка запрета удаления чужого комментария."""
    response = reader_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author


def test_author_can_edit_comment(
        author_client,
        comment,
        edit_url,
        url_to_comments
):
    """Проверка редактирования комментария автором."""
    response = author_client.post(edit_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, url_to_comments)
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == COMMENT_FORM_DATA['text']
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author


def test_user_cant_edit_comment_of_another_user(
        reader_client,
        comment,
        edit_url
):
    """Проверка запрета редактирования чужого комментария."""
    response = reader_client.post(edit_url, data=COMMENT_FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author
