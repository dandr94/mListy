from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass


class EditProfileViewTests(BaseAccountTestClass):
    PATH = 'edit profile'

    TEMPLATE = 'account/edit_profile.html'

    FORM = 'form'

    NEW_VALUES = {
        'first_name': 'editedFirstName',
        'last_name': 'editedLastName',
        'website': 'https://editedwebsite.com',
        'twitter': 'https://editedtwitter.com',
        'instagram': 'https://editedinstagram.com',
        'facebook': 'https://editedfacebook.com'
    }

    def setUp(self):
        self.user, self.profile = self.create_valid_user_and_profile()
        self.login_user()

    def test_correct_template_is_used(self):
        response = self.get_response_for_profile(self.profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_edit_list_with_valid_credentials(self):
        response = self.get_response_for_profile(self.profile)

        expected_website_value = 'http://www.foo@bar.barz'

        self.assertEqual(response.context['profile'].website, expected_website_value)

        form = response.context[self.FORM]
        data = form.initial

        for k in data.keys():
            data[k] = self.NEW_VALUES[k]

        response = self.post_response_for_profile(self.profile, data, follow=True)

        for k in self.NEW_VALUES.keys():
            self.assertEqual(getattr(response.context['profile'], k), self.NEW_VALUES[k])

    def test_redirect_after_valid_edit(self):
        response = self.get_response_for_profile(self.profile)

        form = response.context[self.FORM]
        data = form.initial

        for k in data.keys():
            data[k] = self.NEW_VALUES[k]

        response = self.post_response_for_profile(self.profile, data)
        expected_url = f'/profile/{self.profile.slug}/'

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
