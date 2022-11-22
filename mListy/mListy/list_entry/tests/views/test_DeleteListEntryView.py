from django.urls import reverse

from mListy.list_entry.models import ListEntry
from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass


class DeleteListEntryViewTests(BaseListEntryTestClass):
    TEMPLATE = 'movie/delete_entry.html'

    PATH = 'delete entry'

    def setUp(self):
        super().setUp()
        self.entry = self.create_entry()

    def test_correct_template_is_used(self):
        response = self.get_response_for_list_entry(self.entry)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_delete_entry(self):
        entry = ListEntry.objects.exists()

        self.assertTrue(entry)

        self.post_response_for_list_entry(self.entry, {})

        entry = ListEntry.objects.exists()

        self.assertFalse(entry)

    def test_redirect_after_deletion(self):
        response = self.post_response_for_list_entry(self.entry, {})

        expected_redirect_url = reverse('details list', kwargs={'str': self.user.username, 'slug': self.user_list.slug})

        self.assertRedirects(response, expected_redirect_url)
