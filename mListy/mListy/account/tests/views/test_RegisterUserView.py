from django.contrib.auth import get_user_model
from django.test import TestCase
from mListy.account.tests.utils import VALID_REGISTER_FORM_CREDENTIALS, VALID_USER_CREDENTIALS

UserModel = get_user_model()


class RegisterUserViewTests(TestCase):
    PATH = '/register/'
    REGISTER_TEMPLATE = 'account/register.html'

    def test_correct_page_is_used(self):
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.REGISTER_TEMPLATE)

    def test_register_with_valid_credentials(self):
        self.client.post(self.PATH, data=VALID_REGISTER_FORM_CREDENTIALS)

        user = UserModel.objects.first()

        self.assertIsNotNone(user)
        self.assertEqual(VALID_REGISTER_FORM_CREDENTIALS['username'], user.username)
        self.assertEqual(VALID_REGISTER_FORM_CREDENTIALS['email'], user.email)

    def test_redirect_after_valid_register(self):
        response = self.client.post(self.PATH, data=VALID_REGISTER_FORM_CREDENTIALS)

        expected_url = '/'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
