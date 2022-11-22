from mListy.list_entry.models import ListEntry
from mListy.movie.tests.BaseMovieTest import BaseMovieTest


class DeleteListEntryFormTests(BaseMovieTest):
    PATH = 'delete entry'

    def setUp(self):
        super().setUp()
        self.path = self.get_path(self.PATH, {'pk': self.entry.pk, 'slug': self.entry.slug})

    def test_successful_list_deletion(self):
        entry = ListEntry.objects.filter(pk=self.entry.pk).exists()
        self.assertTrue(entry)

        self.return_post_response({})

        entry = ListEntry.objects.filter(pk=self.entry.pk).exists()
        self.assertFalse(entry)
