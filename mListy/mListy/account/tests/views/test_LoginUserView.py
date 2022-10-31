from django.contrib.auth import get_user_model
from django.test import TestCase

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_LOGIN_CREDENTIALS, VALID_USER_CREDENTIALS

UserModel = get_user_model()


class LoginUserViewTests(TestCase):
    PATH = '/login/'
    REDIRECT_TEMPLATE = 'index.html'

    def setUp(self):
        self.user = UserModel.objects.create_user(
            **VALID_USER_CREDENTIALS)
        self.profile = Profile(user=self.user)
        self.profile.save()

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.PATH, VALID_LOGIN_CREDENTIALS, follow=True)
        self.assertTemplateUsed(response, self.REDIRECT_TEMPLATE)
        self.assertTrue(response.context['user'].is_authenticated)
