from django.urls import reverse

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
        response = self.get_response_for_list(self.user_list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_edit_list_with_valid_credentials(self):
        response = self.get_response_for_list(self.user_list)
        form = response.context[self.FORM]
        data = form.initial

        self.assertContains(response, self.VALID_LIST_DATA[self.TITLE_KEY])

        data[self.TITLE_KEY] = self.NEW_VALUES[self.TITLE_KEY]
        data[self.COVER_KEY] = self.NEW_VALUES[self.COVER_KEY]

        response = self.post_response_for_list(self.user_list, data, follow=True)

        self.assertContains(response, self.NEW_VALUES[self.TITLE_KEY])
        self.assertNotContains(response, self.VALID_LIST_DATA[self.TITLE_KEY])

    def test_redirect_after_valid_edit(self):
        response = self.get_response_for_list(self.user_list)
        form = response.context[self.FORM]
        data = form.initial

        self.assertContains(response, self.VALID_LIST_DATA[self.TITLE_KEY])

        data[self.TITLE_KEY] = self.NEW_VALUES[self.TITLE_KEY]
        data[self.COVER_KEY] = self.NEW_VALUES[self.COVER_KEY]

        response = self.post_response_for_list(self.user_list, data)
        expected_url = '/dashboard/'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_edit_from_request_that_is_not_owner__expect_403(self):
        self.client.logout()

        user2_data = {
            'username': 'brumbroombrim',
            'email': 'brumbroombrim@foo.bar',
            'password': 'hellobye123',
        }

        self.create_user(**user2_data)

        user_2_login_credentials = {
            'username': 'brumbroombrim',
            'password': 'hellobye123'
        }

        self.client.login(**user_2_login_credentials)

        response = self.client.post(reverse(self.PATH, kwargs={'slug': self.user_list.slug}))

        self.assertEqual(response.status_code, 403)