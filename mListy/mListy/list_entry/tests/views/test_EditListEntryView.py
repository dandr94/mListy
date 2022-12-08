from django.urls import reverse
from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass
from mListy.list_entry.tests.utils import VALID_LIST_ENTRY_DATA


class EditListEntryViewTests(BaseListEntryTestClass):
    TEMPLATE = 'list_entry/edit_entry.html'

    PATH = 'edit entry'

    MOCK_WOULD_RECOMMEND = 'No'
    MOCK_GRADE = 10

    DATA_WOULD_RECOMMEND_KEY = 'would_recommend'
    DATA_GRADE_KEY = 'grade'

    def setUp(self):
        super().setUp()
        self.entry = self.create_entry()
        self.FIELD_DATA['list'] = self.user_list.id
        self.FIELD_DATA['movie'] = self.movie

    def test_correct_template_is_used(self):
        response = self.get_response_for_list_entry(self.entry)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_edit_entry_to_list_with_valid_credentials(self):
        response = self.get_response_for_list_entry(self.entry)
        form = response.context[self.FORM]
        data = form.initial

        self.assertEqual(data[self.DATA_WOULD_RECOMMEND_KEY], VALID_LIST_ENTRY_DATA[self.DATA_WOULD_RECOMMEND_KEY])
        self.assertEqual(data[self.DATA_GRADE_KEY], VALID_LIST_ENTRY_DATA[self.DATA_GRADE_KEY])

        data[self.DATA_WOULD_RECOMMEND_KEY] = self.MOCK_WOULD_RECOMMEND
        data[self.DATA_GRADE_KEY] = self.MOCK_GRADE

        response = self.post_response_for_list_entry(self.entry, data, follow=True)

        self.assertContains(response, self.MOCK_GRADE)

    def test_redirect_after_valid_edit(self):
        response = self.get_response_for_list_entry(self.entry)
        form = response.context[self.FORM]
        data = form.initial

        self.assertEqual(data[self.DATA_WOULD_RECOMMEND_KEY], VALID_LIST_ENTRY_DATA[self.DATA_WOULD_RECOMMEND_KEY])
        self.assertEqual(data[self.DATA_GRADE_KEY], VALID_LIST_ENTRY_DATA[self.DATA_GRADE_KEY])

        data[self.DATA_WOULD_RECOMMEND_KEY] = self.MOCK_WOULD_RECOMMEND
        data[self.DATA_GRADE_KEY] = self.MOCK_GRADE

        response = self.post_response_for_list_entry(self.entry, data)

        expected_url = reverse('details list', kwargs={'slug': self.user_list.slug})

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

        response = self.client.post(reverse(self.PATH, kwargs={'pk': self.entry.id, 'slug': self.entry.slug}))

        self.assertEqual(response.status_code, 403)