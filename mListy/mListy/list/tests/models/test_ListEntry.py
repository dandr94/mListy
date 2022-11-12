from django.contrib.auth import get_user_model
from django.test import TestCase

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS
from mListy.list.models import List, ListEntry
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA

UserModel = get_user_model()


class ListEntryTests(TestCase):
    VALID_LIST_TITLE_NAME = 'Drama'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.list = List.objects.create(title=self.VALID_LIST_TITLE_NAME, user=self.user)
        self.list.save()
        self.movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA)
        self.movie.save()
        self.valid_entry_data = {'movie_id': 5,
                                 'movie_name': 'Hello',
                                 'grade': 5,
                                 'list': self.list,
                                 'user': self.user}

    def test_create_list_with_valid_data__expect_correct_values(self):
        entry = ListEntry(**self.valid_entry_data)

        entry.save()

        self.assertIsNotNone(entry.pk)

    def test_create_list_with_valid_data__expect_slug_to_be_correct_value(self):
        entry = ListEntry(**self.valid_entry_data)

        entry.save()
        expected_slug_value = '5-hello'

        self.assertEqual(expected_slug_value, entry.slug)

    def test_return_title(self):
        entry = ListEntry(**self.valid_entry_data)

        entry.save()
        expected_title_value = 'Hello'

        self.assertEqual(expected_title_value, str(entry))
