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
        response = self.client.get(reverse(self.PATH, kwargs={'str': self.profile.slug, 'slug': self.user_list.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_delete_list(self):
        user_list = List.objects.first()

        self.assertTrue(user_list)

        self.post_response_for_list(self.user_list, self.profile, {})

        user_list = List.objects.first()

        self.assertFalse(user_list)

    def test_status_code_after_deletion__expect_302(self):
        response = self.post_response_for_list(self.user_list, self.profile, {})

        self.assertEqual(response.status_code, 302)

    def test_redirect_after_deletion(self):
        response = self.post_response_for_list(self.user_list, self.profile, {})

        expected_redirect_url = reverse('dashboard')

        self.assertRedirects(response, expected_redirect_url)
