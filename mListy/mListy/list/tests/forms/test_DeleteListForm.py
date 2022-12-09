from mListy.list.models import List
from mListy.list.tests.BaseListTestClass import BaseListTestClass


class DeleteListFormTests(BaseListTestClass):
    PATH = 'delete list'

    def setUp(self):
        super().setUp()
        self.user_list = self.create_list(self.user)

    def test_successful_list_deletion(self):
        user_list = List.objects.get(title=self.VALID_LIST_DATA['title'], user=self.user)
        self.assertIsNotNone(user_list)
        self.post_response_for_list(self.user_list, {})
        user_list = List.objects.first()

        self.assertIsNone(user_list)
