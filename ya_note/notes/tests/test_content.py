from notes.forms import NoteForm

from .constants import (
    NOTE_ADD_URL,
    NOTE_EDIT_URL,
    NOTE_SLUG,
    NOTES_LIST_URL,
)
from .test_mixins import BaseTestData


class TestNotesListForDifferentUsers(BaseTestData):
    """Тесты отображения заметок в списке для разных пользователей."""

    def test_author_sees_own_note(self):
        """Автор видит свою заметку в списке."""
        response = self.author_client.get(NOTES_LIST_URL)
        self.assertIn(self.note, response.context['object_list'])
        notes = response.context['object_list'].get(slug=NOTE_SLUG)
        self.assertEqual(notes.title, self.note.title)
        self.assertEqual(notes.text, self.note.text)
        self.assertEqual(notes.slug, self.note.slug)
        self.assertEqual(notes.author, self.note.author)

    def test_not_author_doesnt_see_note(self):
        """Другой пользователь не видит чужую заметку."""
        response = self.not_author_client.get(NOTES_LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])


class TestPagesContainsForm(BaseTestData):
    """Тесты наличия формы на страницах создания и редактирования."""

    def test_pages_contain_form(self):
        """Страницы создания и редактирования содержат форму."""
        urls = (
            NOTE_ADD_URL,
            NOTE_EDIT_URL,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                form = response.context.get('form')
                self.assertIsInstance(form, NoteForm)
