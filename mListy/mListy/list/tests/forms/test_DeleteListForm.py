from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List

UserModel = get_user_model()


class DeleteListFormTests(TestCase):
    VALID_LIST_TITLE_NAME = 'Drama'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.list = List.objects.create(title=self.VALID_LIST_TITLE_NAME, user=self.user)
        self.list.save()
        self.path = reverse('delete list', kwargs={'str': self.user.username, 'slug': self.list.slug})

    def test_successful_list_deletion(self):
        user_list = List.objects.get(title=self.VALID_LIST_TITLE_NAME, user=self.user)
        self.assertIsNotNone(user_list)
        response = self.client.post(self.path)
        user_list = List.objects.first()

        self.assertIsNone(user_list)

