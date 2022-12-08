from django.urls import reverse
from mListy.account.models import Profile
from mListy.account.tests.BaseAccountTestClass import BaseAccountTestClass
from mListy.account.tests.utils import VALID_PROFILE_META_DATA
from mListy.list.models import List
from mListy.list_entry.models import ListEntry
from mListy.list.tests.utils import VALID_LIST_DATA2
from mListy.movie.models import MovieDB
from mListy.movie.tests.utils import VALID_MOVIEDB_DATA_2
from mListy.list_entry.tests.utils import VALID_LIST_ENTRY_DATA_2


class ProfileDetailsViewTests(BaseAccountTestClass):
    PATH = 'details profile'
    TEMPLATE = 'account/details_profile.html'

    CONTEXT_KEY = 'profile'

    def setUp(self):
        self.user, self.profile = self.create_valid_user_and_profile()
        self.login_user()

    def test_when_valid__should_return_correct_template(self):
        response = self.get_response_for_profile(self.profile)

        self.assertTemplateUsed(response, self.TEMPLATE)

    def test_when_opening_valid_profile__expect_200(self):
        response = self.get_response_for_profile(self.profile)

        self.assertEqual(response.status_code, 200)

    def test_when_opening_no_existing_profile__expect_404(self):
        invalid_slug_data = {'slug': 'foobarbarz'}

        response = self.client.get(reverse(self.PATH, kwargs=invalid_slug_data))

        self.assertEqual(response.status_code, 404)

    def test_when_user_is_owner__is_owner_should_be_true(self):
        response = self.get_response_for_profile(self.profile)
        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__is_owner__should_be_false(self):
        credentials = {
            'username': 'foobarz',
            'email': 'barz@barz.foo',
            'password': 'hypermonkey'
        }

        user = self.create_user(**credentials)
        Profile.objects.create(user=user)

        self.logout_user()

        self.client.login(**credentials)

        response = self.get_response_for_profile(self.profile)

        self.assertFalse(response.context['is_owner'])

    def test_profile_with_full_data_expect_correct_values(self):
        response = self.get_response_for_profile(self.profile)

        for k, v in VALID_PROFILE_META_DATA.items():
            self.assertEqual(v, getattr(response.context[self.CONTEXT_KEY], k))

    def test_profile_with_none_data_expect_correct_values(self):
        self.profile.first_name = None
        self.profile.facebook = None
        self.profile.save()

        response = self.get_response_for_profile(self.profile)

        self.assertFalse(response.context[self.CONTEXT_KEY].first_name)
        self.assertFalse(response.context[self.CONTEXT_KEY].facebook)

    def test_profile_details_list_count__expect_1(self):
        self.create_list(self.user)
        response = self.get_response_for_profile(self.profile)

        expected_value = 1

        self.assertEqual(len(response.context_data['user_lists']), expected_value)

    def test_profile_details_list_count__expect_0(self):
        response = self.get_response_for_profile(self.profile)

        expected_value = 0

        self.assertEqual(len(response.context_data['user_lists']), expected_value)

    def test_profile_details_total_movies_count__expect_1(self):
        self.create_list_movie_and_entry(self.user)
        response = self.get_response_for_profile(self.profile)

        expected_value = 1

        self.assertEqual(response.context_data['total_movies'], expected_value)

    def test_profile_details_total_movies_count__expect_0(self):
        response = self.get_response_for_profile(self.profile)

        expected_value = 0

        self.assertEqual(response.context_data['total_movies'], expected_value)

    def test_profile_details_average_grade_with_one_entry__expect_grade_to_be_4(self):
        self.create_list_movie_and_entry(self.user)
        response = self.get_response_for_profile(self.profile)

        expected_value = 4

        self.assertEqual(response.context_data['total_average_grade'], expected_value)

    def test_profile_details_average_grade_with_two_entries__expect_grade_to_be_6(self):
        # entry_1_grade = 4
        # entry_2_grade = 8

        user_list, _, _ = self.create_list_movie_and_entry(self.user)

        movie = MovieDB.objects.create(**VALID_MOVIEDB_DATA_2)
        ListEntry.objects.create(**VALID_LIST_ENTRY_DATA_2, movie=movie, list=user_list)

        response = self.get_response_for_profile(self.profile)

        expected_value = 6

        self.assertEqual(response.context_data['total_average_grade'], expected_value)

    def test_profile_details_average_grade_with_no_entries__expect_0(self):
        response = self.get_response_for_profile(self.profile)

        expected_value = 0

        self.assertEqual(response.context_data['total_average_grade'], expected_value)

    def test_profile_details_last_added_elements(self):
        user_list, movie, entry = self.create_list_movie_and_entry(self.user)

        response = self.get_response_for_profile(self.profile)

        self.assertEqual(response.context['last_added'][0], entry)

    def test_profile_details_last_added_elements_are_sorted_correctly_by_date_created(self):
        _, _, entry = self.create_list_movie_and_entry(
            self.user
        )  # Drama, FooBarBarz, Grade-4

        user_list_2 = List.objects.create(
            **VALID_LIST_DATA2,
            user=self.user
        )  # Fantasy

        movie_2 = MovieDB.objects.create(
            **VALID_MOVIEDB_DATA_2
        )  # 'leetlizard'

        entry_2 = ListEntry.objects.create(
            **VALID_LIST_ENTRY_DATA_2,
            movie=movie_2,
            list=user_list_2)  # Grade-8

        response = self.get_response_for_profile(self.profile)

        self.assertEqual(response.context['last_added'][0], entry_2)
        self.assertEqual(response.context['last_added'][1], entry)
