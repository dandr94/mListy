from django.contrib.auth import get_user_model
from django.test import TestCase

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List

UserModel = get_user_model()


class CreateListViewTests(TestCase):
    PATH = '/create_list/'
    CREATE_LIST_TEMPLATE = 'list/create_list.html'

    VALID_LIST_DATA = {
        'title': 'Drama'
    }

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)

    def test_correct_template_is_used(self):
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.CREATE_LIST_TEMPLATE)

    def test_create_list_with_valid_credentials(self):
        self.client.post(self.PATH, data=self.VALID_LIST_DATA)

        user_list = List.objects.get(title=self.VALID_LIST_DATA['title'], user=self.user)

        self.assertIsNotNone(user_list)
        self.assertEqual(self.VALID_LIST_DATA['title'], user_list.title)

    def test_redirect_after_valid_list_creation(self):
        response = self.client.post(self.PATH, self.VALID_LIST_DATA)
        expected_url = '/dashboard/'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
