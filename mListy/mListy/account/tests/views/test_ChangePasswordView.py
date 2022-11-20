from django.urls import reverse

from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass


class ChangePasswordViewTests(BaseAccountTestClass):
    TEMPLATE = 'account/change_password.html'

    PATH = 'change password'

    VALID_CHANGE_PASSWORD_DATA = {
        'old_password': 'foo123barz1337',
        'new_password1': 'wizardlizzard',
        'new_password2': 'wizardlizzard'
    }

    def setUp(self) -> None:
        self.user, self.profile = self.create_valid_user_and_profile()
        self.login_user()

    def test_correct_template_is_used(self):
        response = self.client.get(reverse(self.PATH))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.TEMPLATE)

    def test_status_code_after_valid_password_change__expect_302(self):
        response = self.client.post(reverse(self.PATH), self.VALID_CHANGE_PASSWORD_DATA)

        self.assertEqual(response.status_code, 302)

    def test_redirect_after_valid_password_change(self):
        response = self.client.post(reverse(self.PATH), self.VALID_CHANGE_PASSWORD_DATA)

        expected_url = reverse('dashboard')

        self.assertRedirects(response, expected_url)

    def test_values_after_valid_password_change(self):
        self.client.post(reverse(self.PATH), self.VALID_CHANGE_PASSWORD_DATA)

        self.assertIn('_auth_user_id', self.client.session)

        self.logout_user()

        self.assertNotIn('_auth_user_id', self.client.session)

        new_valid_login_data = {
            'username': 'foobar',
            'password': 'wizardlizzard'
        }

        self.client.login(**new_valid_login_data)

        self.assertIn('_auth_user_id', self.client.session)
