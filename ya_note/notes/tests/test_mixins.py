from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

from .constants import (
    NEW_NOTE_SLUG,
    NEW_NOTE_TEXT,
    NEW_NOTE_TITLE,
    NOTE_SLUG,
    NOTE_TEXT,
    NOTE_TITLE,
)

User = get_user_model()


class BaseTestData(TestCase):
    """Базовый класс для тестовых данных."""

    @classmethod
    def setUpTestData(cls):
        """Подготовка тестовых данных."""
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = cls.client_class()
        cls.not_author_client.force_login(cls.not_author)

        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.anonymous_client = cls.client_class()

        cls.note = Note.objects.create(
            title=NOTE_TITLE,
            text=NOTE_TEXT,
            slug=NOTE_SLUG,
            author=cls.author
        )

        cls.form_data = {
            'title': NOTE_TITLE,
            'text': NOTE_TEXT,
            'slug': NOTE_SLUG
        }

        cls.new_form_data = {
            'title': NEW_NOTE_TITLE,
            'text': NEW_NOTE_TEXT,
            'slug': NEW_NOTE_SLUG
        }
