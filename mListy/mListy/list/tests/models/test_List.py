from django.contrib.auth import get_user_model
from django.test import TestCase

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS
from mListy.list.models import List

UserModel = get_user_model()


class ListTests(TestCase):
    VALID_TITLE_NAME = 'Drama'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()

    def test_create_list_with_valid_data__expect_correct_values(self):
        movie_list = List(title=self.VALID_TITLE_NAME, user=self.user)

        movie_list.save()

        self.assertIsNotNone(movie_list.pk)

    def test_create_list_with_valid_data__expect_slug_to_be_correct_value(self):
        movie_list = List(title=self.VALID_TITLE_NAME, user=self.user)

        movie_list.save()
        expected_slug_value = 'drama'

        self.assertEqual(expected_slug_value, movie_list.slug)

    def test_return_title(self):
        movie_list = List(title=self.VALID_TITLE_NAME, user=self.user)

        movie_list.save()
        expected_title_value = 'Drama'

        self.assertEqual(expected_title_value, str(movie_list))
