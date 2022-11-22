from django.urls import reverse
from mListy.movie.tests.BaseMovieTest import BaseMovieTest
from mListy.movie.tests.utils import VALID_LIST_ENTRY_DATA


class EditListEntryViewTests(BaseMovieTest):
    TEMPLATE = 'movie/edit_entry.html'

    PATH = 'edit entry'

    MOCK_WOULD_RECOMMEND = 'No'
    MOCK_GRADE = 10

    DATA_WOULD_RECOMMEND_KEY = 'would_recommend'
    DATA_GRADE_KEY = 'grade'

    def setUp(self):
        super().setUp()
        self.path = self.get_path(self.PATH, {'pk': self.entry.pk, 'slug': self.entry.slug})

    def test_correct_template_is_used(self):
        response = self.return_get_response()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_edit_entry_to_list_with_valid_credentials(self):
        response = self.return_get_response()
        form = response.context[self.FORM]
        data = form.initial

        self.assertEqual(data[self.DATA_WOULD_RECOMMEND_KEY], VALID_LIST_ENTRY_DATA[self.DATA_WOULD_RECOMMEND_KEY])
        self.assertEqual(data[self.DATA_GRADE_KEY], VALID_LIST_ENTRY_DATA[self.DATA_GRADE_KEY])

        data[self.DATA_WOULD_RECOMMEND_KEY] = self.MOCK_WOULD_RECOMMEND
        data[self.DATA_GRADE_KEY] = self.MOCK_GRADE

        response = self.client.post(self.path, data, follow=True)

        self.assertContains(response, self.MOCK_GRADE)

    def test_redirect_after_valid_edit(self):
        response = self.return_get_response()
        form = response.context[self.FORM]
        data = form.initial

        self.assertEqual(data[self.DATA_WOULD_RECOMMEND_KEY], VALID_LIST_ENTRY_DATA[self.DATA_WOULD_RECOMMEND_KEY])
        self.assertEqual(data[self.DATA_GRADE_KEY], VALID_LIST_ENTRY_DATA[self.DATA_GRADE_KEY])

        data[self.DATA_WOULD_RECOMMEND_KEY] = self.MOCK_WOULD_RECOMMEND
        data[self.DATA_GRADE_KEY] = self.MOCK_GRADE

        response = self.client.post(self.path, data)

        expected_url = reverse('details list', kwargs={'str': self.user.username, 'slug': self.list.slug})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
