from mListy.list_entry.models import ListEntry
from mListy.list.tests.BaseListTestClass import BaseListTestClass
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA, VALID_MOVIEDB_DATA_2


class DetailsListViewTests(BaseListTestClass):
    TEMPLATE = 'list/details/details_list.html'

    VALID_ENTRY_DATA = {
        'grade': 8,
        'would_recommend': 'Yes',
        'status': 'Completed'
    }

    VALID_ENTRY_DATA_2 = {
        'grade': 4,
        'would_recommend': 'No',
        'status': 'Dropped'
    }

    PATH = 'details list'

    def setUp(self):
        super().setUp()
        self.user_list = self.create_list(self.user)
        self.movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA)
        self.movie_2 = MovieDB.objects.create(**VALID_MOVIEDB_DATA_2)
        self.entry = ListEntry.objects.create(**self.VALID_ENTRY_DATA, movie=self.movie, list=self.user_list)
        self.entry2 = ListEntry.objects.create(**self.VALID_ENTRY_DATA_2, movie=self.movie_2, list=self.user_list)

    def test_correct_template_is_used(self):
        response = self.get_response_for_list(self.user_list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_correct_data_is_listed(self):
        response = self.get_response_for_list(self.user_list)

        entries = [self.entry, self.entry2]
        for i, v in enumerate(response.context['movie_list'].listentry_set.all()):
            self.assertEqual(v.grade, entries[i].grade)
            self.assertEqual(v.would_recommend, entries[i].would_recommend)
            self.assertEqual(v.status, entries[i].status)
            self.assertEqual(v.movie, entries[i].movie)
            self.assertEqual(v.list, entries[i].list)

    def test_total_movies_stats(self):
        response = self.get_response_for_list(self.user_list)

        expected_total_movie_value = 2

        self.assertEqual(len(response.context['movie_list'].listentry_set.all()), expected_total_movie_value)

    def test_time_spend_watching_stats(self):
        response = self.get_response_for_list(self.user_list)

        minutes = self.movie.duration + self.movie_2.duration
        expected_days = minutes // 1440
        left_over_min = minutes % 1440
        expected_hours = left_over_min // 60
        expected_minutes = minutes % 60

        self.assertEqual(response.context['total_time_days'], expected_days)
        self.assertEqual(response.context['total_time_hours'], expected_hours)
        self.assertEqual(response.context['total_time_minutes'], expected_minutes)

    def test_average_grade_stats(self):
        response = self.get_response_for_list(self.user_list)

        expected_average_grade = (self.entry.grade + self.entry2.grade) // 2

        self.assertEqual(response.context['average_grade'], expected_average_grade)
