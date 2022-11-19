from mListy.account.tests.utils import VALID_REGISTER_FORM_CREDENTIALS
from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass


class RegisterUserViewTests(BaseAccountTestClass):
    PATH = 'register'
    TEMPLATE = 'account/register.html'

    def test_correct_template_is_used(self):
        response = self.return_get_response()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_register_with_valid_credentials(self):
        user = self.UserModel.objects.first()

        self.assertIsNone(user)

        self.return_post_response(VALID_REGISTER_FORM_CREDENTIALS)

        user = self.UserModel.objects.first()

        self.assertIsNotNone(user)
        self.assertEqual(VALID_REGISTER_FORM_CREDENTIALS['username'], user.username)
        self.assertEqual(VALID_REGISTER_FORM_CREDENTIALS['email'], user.email)

    def test_redirect_after_valid_register(self):
        response = self.return_post_response(VALID_REGISTER_FORM_CREDENTIALS)

        expected_url = '/dashboard/'

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
