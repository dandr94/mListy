from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass


class EditProfileFormTests(BaseAccountTestClass):
    FORM = 'form'

    PATH = 'edit profile'

    URL_PROFILE_DATA = {
        'facebook': 'https://foo.bar',
        'instagram': 'https://foo.barz',
        'twitter': 'https://foobar.barz',
        'website': ''
    }

    def setUp(self):
        self.user, self.profile = self.create_valid_user_and_profile()
        self.login_user()

    def test_incorrect_url_fields__should_return_correct_error_msg(self):
        expected_field_error_msg = 'Enter a valid URL.'

        for k in self.URL_PROFILE_DATA.keys():
            self.URL_PROFILE_DATA[k] = 'error404'
            response = self.post_response_for_profile(self.profile, self.URL_PROFILE_DATA)
            self.URL_PROFILE_DATA[k] = 'https://foo.bar'  # maybe not needed
            self.assertFormError(response, self.FORM, k, expected_field_error_msg)
