from mListy.movie.tests.BaseMovieTestClass import BaseMovieTestClass
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA


class MovieDetailsViewTests(BaseMovieTestClass):
    DETAILS_MOVIE_TEMPLATE = 'movie/details_movie.html'

    PATH = 'details movie'

    def setUp(self):
        super().setUp()
        self.movie = self.create_movie()

    def test_correct_template_is_used(self):
        response = self.return_get_response(self.movie)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.DETAILS_MOVIE_TEMPLATE)

    def test_correct_data_is_listed(self):
        response = self.return_get_response(self.movie)

        for k in VALID_MOVIEDB_DATA.keys():
            if k != 'release_date':  # FIX
                self.assertEqual(getattr(response.context['movie'], k), VALID_MOVIEDB_DATA[k])
