from django.urls import reverse
from mListy.list.tests.BaseListTestClass import BaseListTestClass


class CreateListFormTests(BaseListTestClass):
    INVALID_LIST_DATA = {
        'title': ''
    }

    PATH = 'create list'

    def setUp(self):
        super().setUp()

    def test_empty_title_field__should_return_correct_error_msg(self):
        field_name_key = 'title'
        expected_empty_field_error_msg = 'This field is required.'

        response = self.client.post(reverse(self.PATH), self.INVALID_LIST_DATA)
        self.assertFormError(response, self.FORM, field_name_key, expected_empty_field_error_msg)

    def test_title_that_already_exists_should_return_correct_error_msg(self):
        self.create_list(self.user)
        expected_unique_error_msg = 'You already have a list with that title. Please choose another.'

        response = self.client.post(reverse(self.PATH), self.VALID_LIST_DATA)

        self.assertFormError(response, self.FORM, None, expected_unique_error_msg)
