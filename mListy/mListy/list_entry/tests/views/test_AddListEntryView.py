from django.urls import reverse
from mListy.list_entry.models import ListEntry
from mListy.movie.tests.BaseMovieTest import BaseMovieTest


class AddListEntryViewTests(BaseMovieTest):
    TEMPLATE = 'movie/add_entry.html'

    PATH = 'add entry'

    def setUp(self):
        super().setUp()
        self.path = self.get_path(self.PATH, {'slug': self.movie.slug})
        self.valid_data = {
            'grade': 8,
            'list': self.list.id,
            'would_recommend': 'Yes',
            'status': 'Completed',
            'movie': self.movie
        }
        ListEntry.objects.all().delete()

    def test_correct_template_is_used(self):
        response = self.return_get_response()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_add_entry_to_list_with_valid_credentials(self):
        self.return_post_response(self.valid_data)
        entry = ListEntry.objects.get(slug=self.movie.slug, list__id=self.list.id)
        self.assertIsNotNone(entry)

    def test_status_code_after_valid_add_entry_to_list_operation__expect_302(self):
        response = self.return_post_response(self.valid_data)
        self.assertEqual(response.status_code, 302)

    def test_redirect_after_valid_add_entry_to_list_operation(self):
        response = self.return_post_response(self.valid_data)
        expected_url = reverse('details movie', kwargs={'slug': self.movie.slug})
        self.assertRedirects(response, expected_url)
