from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS, VALID_PROFILE_META_DATA
from mListy.list.models import List, ListEntry
from mListy.list.tests.utils import VALID_LIST_DATA
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA, VALID_LIST_ENTRY_DATA


class BaseAccountTestClass(TestCase):
    UserModel = get_user_model()

    FORM = ''

    PATH = ''

    TEMPLATE = ''

    def create_user(self, **credentials):
        return self.UserModel.objects.create_user(**credentials)

    def create_valid_user_and_profile(self):
        user = self.create_user(**VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(user=user, **VALID_PROFILE_META_DATA)

        return user, profile

    @staticmethod
    def create_list(user):
        return List.objects.create(**VALID_LIST_DATA, user=user)

    @staticmethod
    def create_movie():
        return MovieDB.objects.create(**VALID_MOVIEDB_DATA)

    def create_list_movie_and_entry(self, user):
        user_list = self.create_list(user)
        movie = self.create_movie()
        entry = ListEntry.objects.create(**VALID_LIST_ENTRY_DATA, movie=movie, list=user_list)

        return user_list, movie, entry

    def login_user(self):
        return self.client.login(**VALID_LOGIN_CREDENTIALS)

    def logout_user(self):
        return self.client.logout()

    def return_post_response(self, credentials, follow=False):
        return self.client.post(reverse(self.PATH), credentials, follow=follow)

    def return_get_response(self, kwargs=None, follow=False):
        return self.client.get(reverse(self.PATH, kwargs=kwargs), follow=follow)

    def get_response_for_profile(self, profile):
        return self.client.get(reverse(self.PATH, kwargs={'slug': profile.slug}))

    def post_response_for_profile(self, profile, credentials, follow=False):
        return self.client.post(reverse(self.PATH, kwargs={'slug': profile.slug}), credentials, follow=follow)
