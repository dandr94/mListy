from mListy.list.tests.BaseListTestClass import BaseListTestClass


class EditListFormTests(BaseListTestClass):
    VALID_LIST_DATA = {
        'title': 'Drama'
    }

    INVALID_LIST_DATA = {
        'title': ''
    }

    PATH = 'edit list'

    def setUp(self):
        super().setUp()
        self.user_list = self.create_list(self.user)

    def test_empty_title_field__should_return_correct_error_msg(self):
        field_name_key = 'title'
        expected_empty_field_error_msg = 'This field is required.'

        response = self.post_response_for_list(self.user_list, self.profile, self.INVALID_LIST_DATA)
        self.assertFormError(response, self.FORM, field_name_key, expected_empty_field_error_msg)

    def test_title_that_already_exists_should_return_correct_error_msg(self):
        expected_unique_error_msg = 'You already have a list with that title. Please choose another.'

        response = self.post_response_for_list(self.user_list, self.profile, self.VALID_LIST_DATA)

        self.assertFormError(response, self.FORM, None, expected_unique_error_msg)
