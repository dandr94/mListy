from django.urls import reverse
from mListy.movie.tests.BaseMovieTestClass import BaseMovieTestClass


class SearchMovieViewTests(BaseMovieTestClass):
    TEMPLATE = 'movie/search_movie.html'

    PATH = 'search movie'

    PAGES = 1

    def setUp(self):
        super().setUp()

    def test_correct_template_is_used(self):
        response = self.client.get(reverse(self.PATH))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)
