from django.test import TestCase
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA

from mListy.movie.models import MovieDB


class MovieDBTests(TestCase):

    def setUp(self):
        self.movie = MovieDB(**VALID_MOVIEDB_DATA)
        self.movie.save()

    def test_movie_with_valid_credentials__expect_valid_save(self):
        self.assertIsNotNone(self.movie.pk)

    def test_return_title(self):
        expected_title_value = 'FooBarBarz'
        self.assertEqual(expected_title_value, str(self.movie))

