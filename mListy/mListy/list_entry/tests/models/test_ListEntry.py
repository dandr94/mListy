from mListy.list_entry.models import ListEntry
from mListy.list.tests.BaseListTestClass import BaseListTestClass
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA


class ListEntryTests(BaseListTestClass):
    VALID_LIST_TITLE_NAME = 'Drama'

    def setUp(self):
        super().setUp()
        self.user_list = self.create_list(self.user)
        self.movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA)
        self.valid_entry_data = {
            'grade': 5,
            'list': self.user_list,
            'movie': self.movie}

    def test_create_list_with_valid_data__expect_correct_values(self):
        ListEntry.objects.create(**self.valid_entry_data)

        entry = ListEntry.objects.get(list_id=self.user_list.id)

        self.assertIsNotNone(entry)

    def test_create_list_with_valid_data__expect_slug_to_be_correct_value(self):
        entry = ListEntry.objects.create(**self.valid_entry_data)

        expected_slug_value = '54212-foobarbarz'

        self.assertEqual(expected_slug_value, entry.slug)

    def test_return_title(self):
        entry = ListEntry.objects.create(**self.valid_entry_data)

        expected_title_value = 'FooBarBarz'

        self.assertEqual(expected_title_value, str(entry))
