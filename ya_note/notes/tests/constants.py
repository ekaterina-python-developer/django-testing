from django.urls import reverse, reverse_lazy

NOTES_LIST_URL = reverse('notes:list')
NOTE_ADD_URL = reverse('notes:add')
NOTE_SLUG = 'test-note'
NOTE_EDIT_URL = reverse('notes:edit', args=[NOTE_SLUG])
NOTE_DETAIL_URL = reverse('notes:detail', args=[NOTE_SLUG])
HOME_URL = reverse('notes:home')
NOTE_SUCCESS_URL = reverse('notes:success')
NOTE_DELETE_URL = reverse('notes:delete', args=[NOTE_SLUG])

NOTE_TITLE = 'Тестовая заметка'
NOTE_TEXT = 'Текст заметки'
NEW_NOTE_TITLE = 'Новый заголовок'
NEW_NOTE_TEXT = 'Новый текст'
NEW_NOTE_SLUG = 'new-note'

LOGIN_URL = reverse_lazy('users:login')
LOGIN_REDIRECT_URL = reverse_lazy('notes:home')
NOTE_COUNT_ON_HOME_PAGE = 10
