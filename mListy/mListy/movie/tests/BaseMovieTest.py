from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List, ListEntry
from mListy.list.tests.utils import VALID_LIST_TITLE_NAME
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA, VALID_LIST_ENTRY_DATA


class BaseMovieTest(TestCase):
    UserModel = get_user_model()

    TEMPLATE = ''

    PATH = ''

    FORM = 'form'

    def setUp(self):
        self.user = self.UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.list = List.objects.create(title=VALID_LIST_TITLE_NAME, user=self.user)
        self.list.save()
        self.movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA)
        self.movie.save()
        VALID_LIST_ENTRY_DATA['list'] = self.list
        VALID_LIST_ENTRY_DATA['user'] = self.user
        self.entry = ListEntry.objects.create(**VALID_LIST_ENTRY_DATA)
        self.entry.save()
        self.path = None

    def get_post_response(self, credentials):
        return self.client.post(self.path, credentials)

    def get_get_response(self):
        return self.client.get(self.path)

    @staticmethod
    def get_path(path, kwargs):
        return reverse(path, kwargs=kwargs)
