from mListy.list_entry.models import ListEntry
from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass
from mListy.list_entry.tests.utils import VALID_LIST_ENTRY_DATA


class ListEntryTests(BaseListEntryTestClass):

    def test_create_list_entry(self):
        entry = ListEntry.objects.first()

        self.assertIsNone(entry)

        self.create_entry()

        entry = ListEntry.objects.first()

        self.assertIsNotNone(entry)

    def test_creat_list_entry__expect_correct_values(self):
        self.create_entry()

        entry = ListEntry.objects.get(list__id=self.user.id)

        expected_slug_value = '54212-foobarbarz'

        self.assertEqual(entry.grade, VALID_LIST_ENTRY_DATA['grade'])
        self.assertEqual(entry.would_recommend, VALID_LIST_ENTRY_DATA['would_recommend'])
        self.assertEqual(entry.status, VALID_LIST_ENTRY_DATA['status'])
        self.assertEqual(entry.movie, self.movie)
        self.assertEqual(entry.list, self.user_list)
        self.assertEqual(entry.slug, expected_slug_value)

    def test_return_title(self):
        entry = self.create_entry()

        expected_title_value = 'FooBarBarz'

        self.assertEqual(expected_title_value, str(entry))
