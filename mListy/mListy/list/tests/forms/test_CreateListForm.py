from django.contrib.auth import get_user_model
from django.test import TestCase
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS

from mListy.account.models import Profile
from mListy.list.models import List

UserModel = get_user_model()


class CreateListFormTests(TestCase):
    VALID_LIST_DATA = {
        'title': 'Drama'
    }

    INVALID_LIST_DATA = {
        'title': ''
    }

    VALID_TITLE_NAME = 'Drama'

    PATH = '/create_list/'
    FORM = 'form'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)

    def __get_response(self, credentials):
        return self.client.post(self.PATH, credentials)

    def test_empty_title_field__should_return_correct_error_msg(self):
        field_name_key = 'title'
        expected_empty_field_error_msg = 'This field is required.'

        response = self.__get_response(self.INVALID_LIST_DATA)
        self.assertFormError(response, self.FORM, field_name_key, expected_empty_field_error_msg)

    def test_title_that_already_exists_should_return_correct_error_msg(self):
        movie_list = List(title=self.VALID_TITLE_NAME, user=self.user)
        movie_list.save()
        expected_unique_error_msg = 'You already have a list with that title. Please choose another.'

        response = self.__get_response(self.VALID_LIST_DATA)

        self.assertFormError(response, self.FORM, None, expected_unique_error_msg)
