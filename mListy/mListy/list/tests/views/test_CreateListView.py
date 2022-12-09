from django.urls import reverse
from mListy.account.tests.utils import VALID_LOGIN_CREDENTIALS
from mListy.list.models import List
from mListy.list.tests.BaseListTestClass import BaseListTestClass


class CreateListViewTests(BaseListTestClass):
    PATH = 'create list'

    TEMPLATE = 'list/create_list.html'

    def setUp(self):
        super().setUp()
        self.client.login(**VALID_LOGIN_CREDENTIALS)

    def test_correct_template_is_used(self):
        response = self.client.get(reverse(self.PATH))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_create_list_with_valid_credentials(self):
        self.post_response_for_create_list(self.VALID_LIST_DATA)

        user_list = List.objects.get(title=self.VALID_LIST_DATA['title'], user=self.user)

        self.assertIsNotNone(user_list)
        self.assertEqual(self.VALID_LIST_DATA['title'], user_list.title)

    def test_status_code_after_valid_list_creation__expect_302(self):
        response = self.post_response_for_create_list(self.VALID_LIST_DATA)
        self.assertEqual(response.status_code, 302)

    def test_redirect_after_valid_list_creation(self):
        response = self.post_response_for_create_list(self.VALID_LIST_DATA)
        expected_url = '/dashboard/'
        self.assertRedirects(response, expected_url)
