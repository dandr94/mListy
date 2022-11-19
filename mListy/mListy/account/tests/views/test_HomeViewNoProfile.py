from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass

class HomeViewNoProfileTests(BaseAccountTestClass):
    PATH = 'index'
    TEMPLATE = 'index.html'
    DASHBOARD_TEMPLATE = 'dashboard.html'

    def setUp(self) -> None:
        self.user, self.profile = self.create_valid_user_and_profile()

    def test_user_is_not_authenticated__expect_correct_template(self):
        response = self.return_get_response()

        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_user_is_authenticated__expect_correct_redirect_template(self):
        self.login_user()

        response = self.return_get_response(follow=True)

        self.assertTemplateUsed(response, self.DASHBOARD_TEMPLATE)

    def test_redirect_when_user_is_authenticated__expect_correct_status_code(self):
        self.login_user()

        response = self.return_get_response()

        self.assertEqual(response.status_code, 302)
