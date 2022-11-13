from django.urls import reverse

from mListy.list.models import ListEntry
from mListy.movie.tests.BaseMovieTest import BaseMovieTest


class DeleteListEntryViewTests(BaseMovieTest):
    TEMPLATE = 'movie/delete_entry.html'

    PATH = 'delete entry'

    def setUp(self):
        super().setUp()
        self.path = self.get_path(self.PATH, {'pk': self.entry.pk, 'slug': self.entry.slug})

    def test_correct_template_is_used(self):
        response = self.get_get_response()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_delete_entry(self):
        entry = ListEntry.objects.exists()

        self.assertTrue(entry)

        self.get_post_response({})

        entry = ListEntry.objects.exists()

        self.assertFalse(entry)

    def test_redirect_after_deletion(self):
        response = self.get_post_response({})

        expected_redirect_url = reverse('details list', kwargs={'str': self.user.username, 'slug': self.list.slug})

        self.assertRedirects(response, expected_redirect_url)
