from django.contrib.auth import get_user_model
from django.test import TestCase
from mListy.account.models import mListyUser
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_REGISTER_FORM_CREDENTIALS

UserModel = get_user_model()


class CreateUserFormTests(TestCase):
    MOCK_UP_DATA = {
        'username': '',
        'email': '',
        'password1': '',
        'password2': ''
    }

    PATH = '/register/'
    FORM = 'form'
    EXPECTED_EMPTY_FIELD_ERROR_MSG = 'This field is required.'

    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def __get_response(self, credentials):
        return self.client.post(self.PATH, credentials)

    def test_empty_username_field__should_return_correct_error_msg(self):
        field_name_key = 'username'
        response = self.__get_response(self.MOCK_UP_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EXPECTED_EMPTY_FIELD_ERROR_MSG)

    def test_empty_email_field__should_return_correct_error_msg(self):
        field_name_key = 'email'
        response = self.__get_response(self.MOCK_UP_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EXPECTED_EMPTY_FIELD_ERROR_MSG)

    def test_empty_password1_field__should_return_correct_error_msg(self):
        field_name_key = 'password1'
        response = self.__get_response(self.MOCK_UP_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EXPECTED_EMPTY_FIELD_ERROR_MSG)

    def test_empty_password2_field__should_return_correct_error_msg(self):
        field_name_key = 'password2'
        response = self.__get_response(self.MOCK_UP_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EXPECTED_EMPTY_FIELD_ERROR_MSG)

    def test_already_in_use_username__should_return_correct_error_msg(self):
        field_name_key = 'username'
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        response = self.__get_response(VALID_REGISTER_FORM_CREDENTIALS)
        self.assertFormError(response, self.FORM, field_name_key, mListyUser.USERNAME_UNIQUE_ERROR_MESSAGE)

    def test_already_is_use_email__should_return_correct_error_msg(self):
        field_name_key = 'email'
        post_credentials = {'email': 'foo@bar.barz'}
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        response = self.__get_response(post_credentials)
        self.assertFormError(response, self.FORM, field_name_key, mListyUser.EMAIL_UNIQUE_ERROR_MESSAGE)

    def test_password_does_not_match__should_return_correct_error_msg(self):
        field_name_key = 'password2'
        post_credentials = {'username': 'foobar',
                            'email': 'foo123@bar.barz',
                            'password1': 'foobarbarz',
                            'password2': 'barz134foo'}
        expected_error_msg = 'The two password fields didn’t match.'
        response = self.__get_response(post_credentials)
        self.assertFormError(response, self.FORM, field_name_key, expected_error_msg)
