from audioop import reverse

from mListy.account.tests.utils import VALID_LOGIN_CREDENTIALS, VALID_USER_CREDENTIALS
from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass


class LoginUserViewTests(BaseAccountTestClass):
    PATH = 'login'
    TEMPLATE = 'account/login.html'

    def setUp(self) -> None:
        self.user, self.profile = self.create_valid_user_and_profile()

    def test_correct_template_is_used(self):
        response = self.return_get_response()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_login_with_valid_credentials(self):
        self.return_post_response(VALID_LOGIN_CREDENTIALS)

        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_status_code_after_valid_login__expect_302(self):
        response = self.return_post_response(VALID_LOGIN_CREDENTIALS)

        expected_status_code = 302

        self.assertEqual(response.status_code, expected_status_code)

    def test_redirect_after_valid_login(self):
        response = self.return_post_response(VALID_LOGIN_CREDENTIALS)

        expected_url = '/dashboard/'

        self.assertRedirects(response, expected_url)

