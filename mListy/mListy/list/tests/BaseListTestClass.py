from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List
from mListy.list.tests.utils import VALID_LIST_DATA


class BaseListTestClass(TestCase):
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

    def create_user(self, **credentials):
        return self.UserModel.objects.create_user(**credentials)

    @staticmethod
    def create_list(user):
        return List.objects.create(**VALID_LIST_DATA, user=user)

    def get_response_for_list(self, user_list,):
        return self.client.get(reverse(self.PATH, kwargs={'slug': user_list.slug}))

    def post_response_for_list(self, user_list, credentials, follow=False):
        return self.client.post(reverse(self.PATH, kwargs={'slug': user_list.slug}),
                                credentials,
                                follow=follow)
