from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA


class BaseMovieTestClass(TestCase):
    UserModel = get_user_model()

    TEMPLATE = ''

    PATH = ''

    FORM = 'form'

    def setUp(self):
        self.user = self.UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.client.login(**VALID_LOGIN_CREDENTIALS)

    @staticmethod
    def create_movie():
        return MovieDB.objects.create(**VALID_MOVIEDB_DATA)

    def return_get_response(self, movie):
        return self.client.get(reverse(self.PATH, kwargs={'slug': movie.slug}))
