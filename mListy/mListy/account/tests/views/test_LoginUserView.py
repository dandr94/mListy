from django.contrib.auth import get_user_model
from django.test import TestCase
from mListy.account.tests.utils import VALID_LOGIN_CREDENTIALS, VALID_USER_CREDENTIALS

UserModel = get_user_model()


class LoginUserViewTests(TestCase):
    PATH = '/login/'

    def setUp(self):
        self.user = UserModel.objects.create_user(
            **VALID_USER_CREDENTIALS)

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.PATH, VALID_LOGIN_CREDENTIALS, follow=True)
        self.assertTrue(response.context['user'].is_active)
