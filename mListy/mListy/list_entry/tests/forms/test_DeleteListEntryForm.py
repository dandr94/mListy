from mListy.list_entry.models import ListEntry
from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass


class DeleteListEntryFormTests(BaseListEntryTestClass):
    PATH = 'delete entry'

    def setUp(self):
        super().setUp()
        self.entry = self.create_entry()

    def test_successful_list_deletion(self):
        entry = ListEntry.objects.first()

        self.assertTrue(entry)

        self.post_response_for_list_entry(self.entry, {})

        entry = ListEntry.objects.first()
        self.assertFalse(entry)
