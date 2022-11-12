from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List, ListEntry
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA

UserModel = get_user_model()


class AddMovieToListFormTests(TestCase):
    ADD_MOVIE_TO_LIST_TEMPLATE = 'movie/add_movie_to_list.html'

    VALID_LIST_TITLE_NAME = 'Drama'

    FORM = 'form'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.list = List.objects.create(title=self.VALID_LIST_TITLE_NAME, user=self.user)
        self.list.save()
        self.movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA)
        self.movie.save()
        self.path = reverse('add movie to list', kwargs={'slug': self.movie.slug})
        self.valid_data = {
            'grade': 5,
            'list': self.list.id,
            'would_recommend': 'No'
        }

    def __get_response(self, credentials):
        return self.client.post(self.path, credentials)

    def test_correct_template_is_used(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.ADD_MOVIE_TO_LIST_TEMPLATE)

    def test_add_movie_to_list_with_valid_credentials(self):
        response = self.__get_response(self.valid_data)
        entry = ListEntry.objects.get(list=self.list, user=self.user)
        self.assertIsNotNone(entry)

    def test_status_code_after_valid_add_movie_to_list_operation__expect_302(self):
        response = self.__get_response(self.valid_data)
        self.assertEqual(response.status_code, 302)

    def test_redirect_after_valid_add_movie_to_list_operation(self):
        response = self.__get_response(self.valid_data)
        expected_url = reverse('details movie', kwargs={'slug': self.movie.slug})
        self.assertRedirects(response, expected_url)


