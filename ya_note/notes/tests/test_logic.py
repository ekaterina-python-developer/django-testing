from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note

from .constants import (
    NOTE_ADD_URL,
    NOTE_DELETE_URL,
    NOTE_EDIT_URL,
    NOTE_SUCCESS_URL,
)
from .test_mixins import BaseTestData


class TestNoteOperations(BaseTestData):
    """Тесты для операций с заметками: создание, редактирование, удаление."""

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        initial_notes = set(Note.objects.values_list('pk', flat=True))
        self.anonymous_client.post(NOTE_ADD_URL, data=self.form_data)
        current_notes = set(Note.objects.values_list('pk', flat=True))
        self.assertSetEqual(initial_notes, current_notes)

    def test_authorized_user_can_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        notes_before = set(Note.objects.values_list('id', flat=True))
        response = self.author_client.post(
            NOTE_ADD_URL, data=self.new_form_data)
        notes_after = Note.objects.exclude(id__in=notes_before)
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        self.assertEqual(notes_after.count(), 1)

        new_note = notes_after.first()
        for field in ('title', 'text', 'slug'):
            self.assertEqual(getattr(new_note, field),
                             self.new_form_data[field])
        self.assertEqual(new_note.author, self.author)

    def test_slug_is_generated_automatically_if_missing(self):
        """Slug генерируется автоматически, если он не передан в форме."""
        data = self.new_form_data.copy()
        data.pop('slug')
        response = self.author_client.post(NOTE_ADD_URL, data=data)
        self.assertRedirects(response, NOTE_SUCCESS_URL)

        expected_slug = slugify(data['title'])
        created_note = Note.objects.get(slug=expected_slug)

        for field in ('title', 'text'):
            self.assertEqual(getattr(created_note, field), data[field])
        self.assertEqual(created_note.author, self.author)

    def test_user_cannot_create_note_with_duplicate_slug(self):
        """Нельзя создать заметку с уже существующим slug."""
        response = self.author_client.post(NOTE_ADD_URL, data=self.form_data)
        form = response.context['form']

        self.assertIn('slug', form.errors)
        self.assertIn(self.form_data['slug'], form.errors['slug'][0])

        self.assertEqual(Note.objects.filter(
            slug=self.form_data['slug']).count(), 1)

    def test_author_can_edit_note(self):
        """Автор может отредактировать свою заметку."""
        response = self.author_client.post(
            NOTE_EDIT_URL, data=self.new_form_data)
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        edited_note = Note.objects.get(pk=self.note.pk)
        for field in ('title', 'text', 'slug'):
            self.assertEqual(getattr(edited_note, field),
                             self.new_form_data[field])
        self.assertEqual(edited_note.author, self.author)

    def test_user_cannot_edit_others_note(self):
        """Пользователь не может редактировать чужую заметку."""
        original_data = {
            'title': self.note.title,
            'text': self.note.text,
            'slug': self.note.slug,
            'author': self.note.author
        }
        response = self.reader_client.post(
            NOTE_EDIT_URL, data=self.new_form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        unchanged_note = Note.objects.get(pk=self.note.pk)
        for key in original_data:
            self.assertEqual(getattr(unchanged_note, key), original_data[key])

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку."""
        note_id = self.note.pk
        response = self.author_client.delete(NOTE_DELETE_URL)
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(pk=note_id).exists())

    def test_user_cannot_delete_others_note(self):
        """Пользователь не может удалить чужую заметку."""
        notes_before = list(Note.objects.values(
            'title', 'text', 'slug', 'author'))
        response = self.reader_client.delete(NOTE_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = list(Note.objects.values(
            'title', 'text', 'slug', 'author'))
        self.assertEqual(notes_before, notes_after)
