from django.urls import reverse

from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass


class ChangePasswordFormTests(BaseAccountTestClass):
    FORM = 'form'

    PATH = 'change password'

    EXPECTED_EMPTY_FIELD_ERROR_MSG = 'This field is required.'

    EMPTY_FIELD_DATA = {
        'old_password': '',
        'new_password1': '',
        'new_password2': ''
    }

    def setUp(self) -> None:
        self.user, self.profile = self.create_valid_user_and_profile()
        self.login_user()

    def test_empty_fields__should_return_correct_error_msg(self):
        response = self.client.post(reverse(self.PATH), self.EMPTY_FIELD_DATA)
        for k in self.EMPTY_FIELD_DATA.keys():
            self.assertFormError(response, self.FORM, k, self.EXPECTED_EMPTY_FIELD_ERROR_MSG)

    def test_old_password_field_with_wrong_value__expect_correct_error_msg(self):
        wrong_password_data = {'old_password': 'foooo'}
        field_name_key = 'old_password'

        response = self.client.post(reverse(self.PATH), wrong_password_data)

        expected_error_msg = 'Your old password was entered incorrectly. Please enter it again.'

        self.assertFormError(response, self.FORM, field_name_key, expected_error_msg)

    def test_non_matching_new_password_fields_expect_correct_error_msg(self):
        wrong_password_data = {'old_password': 'foo123barz1337',
                               'new_password1': 'wizardlizzard',
                               'new_password2': 'brumvroom'}
        field_name_key = 'new_password2'

        response = self.client.post(reverse(self.PATH), wrong_password_data)

        expected_error_msg = 'The two password fields didn’t match.'

        self.assertFormError(response, self.FORM, field_name_key, expected_error_msg)


