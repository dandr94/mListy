from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA

UserModel = get_user_model()


class MovieDetailsViewTests(TestCase):
    DETAILS_MOVIE_TEMPLATE = 'movie/details_movie.html'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.movie = MovieDB(**VALID_MOVIEDB_DATA)
        self.movie.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.path = reverse('details movie', kwargs={'slug': self.movie.slug})

    def test_correct_template_is_user(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.DETAILS_MOVIE_TEMPLATE)

    def test_correct_data_is_listed(self):
        response = self.client.get(self.path)
        self.assertEqual(response.context['movie'].movie_id, VALID_MOVIEDB_DATA['movie_id'])
        self.assertEqual(response.context['movie'].name, VALID_MOVIEDB_DATA['name'])
        self.assertEqual(response.context['movie'].poster, VALID_MOVIEDB_DATA['poster'])
        self.assertEqual(response.context['movie'].description, VALID_MOVIEDB_DATA['description'])
        self.assertEqual(response.context['movie'].duration, VALID_MOVIEDB_DATA['duration'])
        self.assertEqual(response.context['movie'].genres, VALID_MOVIEDB_DATA['genres'])
        self.assertEqual(response.context['movie'].average_grade, VALID_MOVIEDB_DATA['average_grade'])
        self.assertEqual(response.context['movie'].actors, VALID_MOVIEDB_DATA['actors'])
        self.assertEqual(response.context['movie'].roles, VALID_MOVIEDB_DATA['roles'])
        self.assertEqual(response.context['movie'].production_companies, VALID_MOVIEDB_DATA['production_companies'])
        self.assertEqual(response.context['movie'].language, VALID_MOVIEDB_DATA['language'])
        self.assertEqual(response.context['movie'].imdb_link, VALID_MOVIEDB_DATA['imdb_link'])
        self.assertEqual(response.context['movie'].budget, VALID_MOVIEDB_DATA['budget'])
        self.assertEqual(response.context['movie'].status, VALID_MOVIEDB_DATA['status'])
