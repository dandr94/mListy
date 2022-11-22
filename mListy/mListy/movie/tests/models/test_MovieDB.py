from mListy.movie.models import MovieDB
from mListy.movie.tests.BaseMovieTestClass import BaseMovieTestClass
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA


class MovieDBTests(BaseMovieTestClass):

    def test_movie_with_valid_credentials__expect_valid_save(self):
        movie = MovieDB.objects.first()

        self.assertIsNone(movie)

        movie = self.create_movie()

        self.assertIsNotNone(movie.pk)

    def test_movie_values(self):
        movie = self.create_movie()

        for k in VALID_MOVIEDB_DATA.keys():
            self.assertEqual(getattr(movie, k), VALID_MOVIEDB_DATA[k])

    def test_slug(self):
        movie = self.create_movie()

        expected_slug_value = '54212-foobarbarz'

        self.assertEqual(expected_slug_value, movie.slug)

    def test_return_title(self):
        movie = self.create_movie()

        expected_title_value = 'FooBarBarz'

        self.assertEqual(expected_title_value, str(movie))
