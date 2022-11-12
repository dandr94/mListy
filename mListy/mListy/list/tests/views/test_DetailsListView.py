from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List, ListEntry
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA

UserModel = get_user_model()


class DetailsListViewTests(TestCase):
    DETAILS_MOVIE_TEMPLATE = 'list/list_details.html'
    VALID_LIST_TITLE_NAME = 'Drama'

    VALID_ENTRY_DATA = {
        'movie_id': 10,
        'movie_name': 'Ice Age',
        'grade': 8,
        'would_recommend': 'Yes'
    }

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.list = List.objects.create(title=self.VALID_LIST_TITLE_NAME, user=self.user)
        self.list.save()
        self.movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA)
        self.movie.save()
        self.entry = ListEntry.objects.create(**{
            'movie_id': self.movie.id,
            'movie_name': self.movie.name,
            'grade': 5,
            'would_recommend': 'No',
            'list': self.list,
            'user': self.user
        })
        self.entry2 = ListEntry.objects.create(**{
            'movie_id': self.VALID_ENTRY_DATA['movie_id'],
            'movie_name': self.VALID_ENTRY_DATA['movie_name'],
            'grade': self.VALID_ENTRY_DATA['grade'],
            'would_recommend': self.VALID_ENTRY_DATA['would_recommend'],
            'list': self.list,
            'user': self.user
        })
        self.path = reverse('details list', kwargs={'str': self.user.username, 'slug': self.list.slug})

    def test_correct_template_is_used(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.DETAILS_MOVIE_TEMPLATE)

    def test_correct_data_is_listed(self):
        response = self.client.get(self.path)

        entries = [self.entry, self.entry2]
        for i in range(len(entries)):
            self.assertEqual(response.context['movie_list'][i].movie_id, entries[i].movie_id)
            self.assertEqual(response.context['movie_list'][i].movie_name, entries[i].movie_name)
            self.assertEqual(response.context['movie_list'][i].grade, entries[i].grade)
            self.assertEqual(response.context['movie_list'][i].would_recommend, entries[i].would_recommend)

