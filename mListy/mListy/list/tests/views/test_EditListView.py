from mListy.list.tests.BaseListTestClass import BaseListTestClass


class EditListViewTests(BaseListTestClass):
    TEMPLATE = 'list/edit_list.html'

    PATH = 'edit list'

    TITLE_KEY = 'title'
    COVER_KEY = 'cover'

    VALID_LIST_DATA = {
        TITLE_KEY: 'Drama',
        COVER_KEY: ''
    }

    NEW_VALUES = {
        TITLE_KEY: 'Horror',
        COVER_KEY: 'https://editedwebsite.com',
    }

    def setUp(self):
        super().setUp()
        self.user_list = self.create_list(self.user)

    def test_correct_template_is_used(self):
        response = self.get_response_for_list(self.user_list, self.profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_edit_list_with_valid_credentials(self):
        response = self.get_response_for_list(self.user_list, self.profile)
        form = response.context[self.FORM]
        data = form.initial

        self.assertContains(response, self.VALID_LIST_DATA[self.TITLE_KEY])

        data[self.TITLE_KEY] = self.NEW_VALUES[self.TITLE_KEY]
        data[self.COVER_KEY] = self.NEW_VALUES[self.COVER_KEY]

        response = self.post_response_for_list(self.user_list, self.profile, data, follow=True)

        self.assertContains(response, self.NEW_VALUES[self.TITLE_KEY])
        self.assertNotContains(response, self.VALID_LIST_DATA[self.TITLE_KEY])

    def test_redirect_after_valid_edit(self):
        response = self.get_response_for_list(self.user_list, self.profile)
        form = response.context[self.FORM]
        data = form.initial

        self.assertContains(response, self.VALID_LIST_DATA[self.TITLE_KEY])

        data[self.TITLE_KEY] = self.NEW_VALUES[self.TITLE_KEY]
        data[self.COVER_KEY] = self.NEW_VALUES[self.COVER_KEY]

        response = self.post_response_for_list(self.user_list, self.profile, data)
        expected_url = '/dashboard/'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
