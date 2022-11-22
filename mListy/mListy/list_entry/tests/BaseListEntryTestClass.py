from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List
from mListy.list.tests.utils import VALID_LIST_DATA
from mListy.list_entry.models import ListEntry
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA
from mListy.list_entry.tests.utils import VALID_LIST_ENTRY_DATA


class BaseListEntryTestClass(TestCase):
    UserModel = get_user_model()

    TEMPLATE = ''

    PATH = ''

    FORM = 'form'

    FIELD_DATA = {
        'grade': '4',
        'would_recommend': 'Yes',
        'status': 'Completed'
    }

    def setUp(self):
        self.user = self.UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.user_list = List.objects.create(**VALID_LIST_DATA, user=self.user)
        self.movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA)

    def create_entry(self):
        return ListEntry.objects.create(**VALID_LIST_ENTRY_DATA, movie=self.movie, list=self.user_list)

    def post_response_for_create_list_entry(self, movie, credentials):
        return self.client.post(reverse(self.PATH, kwargs={'slug': movie.slug}), credentials)

    def get_response_for_list_entry(self, entry):
        return self.client.get(reverse(self.PATH, kwargs={'pk': entry.id, 'slug': entry.movie.slug}))

    def post_response_for_list_entry(self, entry, credentials, follow=False):
        return self.client.post(reverse(self.PATH, kwargs={'pk': entry.id, 'slug': entry.list.slug}),
                                credentials,
                                follow=follow)
