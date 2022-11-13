from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA

UserModel = get_user_model()


class AddMovieToListFormTests(TestCase):
    VALID_LIST_TITLE_NAME = 'Drama'

    INVALID_GRADE_FIELD_DATA = {
        'grade': '',
        'list': 'Drama',
        'would_recommend': 'Yes'
    }

    INVALID_LIST_FIELD_DATA = {
        'grade': 5,
        'list': '',
        'would_recommend': 'Yes'
    }

    FORM = 'form'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.list = List(title=self.VALID_LIST_TITLE_NAME, user=self.user)
        self.list.save()
        self.movie = MovieDB(**VALID_MOVIEDB_DATA)
        self.movie.save()
        self.path = reverse('add movie to list', kwargs={'slug': self.movie.slug})

    def __get_response(self, credentials):
        return self.client.post(self.path, credentials)

    def test_empty_grade_field__should_return_correct_error_msg(self):
        field_name_key = 'grade'
        expected_empty_field_error_msg = 'This field is required.'

        response = self.__get_response(self.INVALID_GRADE_FIELD_DATA)
        self.assertFormError(response, self.FORM, field_name_key, expected_empty_field_error_msg)

    def test_empty_list_field__should_return_correct_error_msg(self):
        field_name_key = 'list'
        expected_empty_field_error_msg = 'This field is required.'

        response = self.__get_response(self.INVALID_LIST_FIELD_DATA)
        self.assertFormError(response, self.FORM, field_name_key, expected_empty_field_error_msg)