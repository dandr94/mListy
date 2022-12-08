from django.urls import reverse
from mListy.list.models import List
from mListy.list.tests.BaseListTestClass import BaseListTestClass


class DeleteListViewTests(BaseListTestClass):
    VALID_LIST_DATA = {
        'title': 'Drama'
    }
    TEMPLATE = 'list/delete_list.html'

    PATH = 'delete list'

    def setUp(self):
        super().setUp()
        self.user_list = self.create_list(self.user)

    def test_correct_template_is_used(self):
        response = self.client.get(reverse(self.PATH, kwargs={'slug': self.user_list.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_delete_list(self):
        user_list = List.objects.first()

        self.assertTrue(user_list)

        self.post_response_for_list(self.user_list, {})

        user_list = List.objects.first()

        self.assertFalse(user_list)

    def test_status_code_after_deletion__expect_302(self):
        response = self.post_response_for_list(self.user_list, {})

        self.assertEqual(response.status_code, 302)

    def test_redirect_after_deletion(self):
        response = self.post_response_for_list(self.user_list, {})

        expected_redirect_url = reverse('dashboard')

        self.assertRedirects(response, expected_redirect_url)

    def test_delete_from_request_that_is_not_owner__expect_403(self):
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
