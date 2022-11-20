from mListy.list.models import List
from mListy.list.tests.BaseListTestClass import BaseListTestClass


class ListTests(BaseListTestClass):
    VALID_TITLE_NAME = 'Drama'

    def setUp(self):
        super().setUp()

    def test_create_list_with_valid_data__expect_correct_values(self):
        List.objects.create(title=self.VALID_TITLE_NAME, user=self.user)

        user_list = List.objects.get(title=self.VALID_TITLE_NAME, user=self.user)

        self.assertIsNotNone(user_list)

    def test_create_list_with_valid_data__expect_slug_to_be_correct_value(self):
        user_list = List.objects.create(title=self.VALID_TITLE_NAME, user=self.user)

        expected_slug_value = 'drama'

        self.assertEqual(expected_slug_value, user_list.slug)

    def test_return_title(self):
        user_list = List.objects.create(title=self.VALID_TITLE_NAME, user=self.user)

        expected_title_value = 'Drama'

        self.assertEqual(expected_title_value, str(user_list))
