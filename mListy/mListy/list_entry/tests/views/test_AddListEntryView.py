from django.urls import reverse
from mListy.list_entry.models import ListEntry
from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass
from mListy.list_entry.tests.utils import VALID_LIST_ENTRY_DATA_2


class AddListEntryViewTests(BaseListEntryTestClass):
    TEMPLATE = 'list_entry/add_entry.html'

    PATH = 'add entry'

    def setUp(self):
        super().setUp()
        VALID_LIST_ENTRY_DATA_2['list'] = self.user_list.id
        VALID_LIST_ENTRY_DATA_2['movie'] = self.movie

    def test_correct_template_is_used(self):
        response = self.client.get(reverse(self.PATH, kwargs={'slug': self.movie.slug}))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_add_entry_to_list_with_valid_credentials(self):
        self.post_response_for_create_list_entry(self.movie, VALID_LIST_ENTRY_DATA_2)

        entry = ListEntry.objects.get(slug=self.movie.slug, list__id=self.user_list.id)

        self.assertIsNotNone(entry)

    def test_status_code_after_valid_add_entry_to_list_operation__expect_302(self):
        response = self.post_response_for_create_list_entry(self.movie, VALID_LIST_ENTRY_DATA_2)

        self.assertEqual(response.status_code, 302)

    def test_redirect_after_valid_add_entry_to_list_operation(self):
        response = self.post_response_for_create_list_entry(self.movie, VALID_LIST_ENTRY_DATA_2)

        expected_url = reverse('details movie', kwargs={'slug': self.movie.slug})

        self.assertRedirects(response, expected_url)
