from django.contrib.auth import get_user_model
from django.test import TestCase
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS

from mListy.account.models import Profile

UserModel = get_user_model()


class HomeViewNoProfileTests(TestCase):
    PATH = '/'
    INDEX_TEMPLATE = 'index.html'
    DASHBOARD_TEMPLATE = 'dashboard.html'

    def test_user_is_not_authenticated__expect_correct_template(self):
        response = self.client.get(self.PATH)

        self.assertTemplateUsed(response, self.INDEX_TEMPLATE)

    def test_user_is_authenticated__expect_correct_template(self):
        user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            user=user
        )
        profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)

        response = self.client.get(self.PATH, follow=True)

        self.assertTemplateUsed(response, self.DASHBOARD_TEMPLATE)

    def test_redirect_when_user_is_authenticated__expect_correct_status_code(self):
        user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            user=user
        )
        profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)

        response = self.client.get(self.PATH)

        self.assertEqual(response.status_code, 302)
