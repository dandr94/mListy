from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS, VALID_PROFILE_META_DATA

UserModel = get_user_model()


class ProfileDetailsViewTests(TestCase):
    PATH = 'profile details'
    PROFILE_TEMPLATE = 'account/profile_details.html'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(**VALID_PROFILE_META_DATA, user=self.user)
        self.profile.save()

    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(user=user)

        return user, profile

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse(self.PATH, kwargs={'slug': profile.slug}))

    def test_when_valid__should_return_correct_template(self):
        response = self.__get_response_for_profile(self.profile)
        self.assertTemplateUsed(response, self.PROFILE_TEMPLATE)

    def test_when_opening_valid_profile__expect_200(self):
        valid_slug_data = {'slug': self.user.username}

        response = self.client.get(reverse(self.PATH, kwargs=valid_slug_data))
        self.assertEqual(response.status_code, 200)

    def test_when_opening_no_existing_profile__expect_404(self):
        invalid_slug_data = {'slug': 'foobarbarz'}

        response = self.client.get(reverse(self.PATH, kwargs=invalid_slug_data))
        self.assertEqual(response.status_code, 404)

    def test_when_user_is_owner__is_owner_should_be_true(self):
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        response = self.__get_response_for_profile(self.profile)
        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__is_owner__should_be_false(self):
        credentials = {
            'username': 'foobarz',
            'email': 'barz@barz.foo',
            'password': 'hypermonkey'
        }
        user = self.__create_user(**credentials)
        profile = Profile(user=user)
        profile.save()

        self.client.login(**credentials)

        response = self.__get_response_for_profile(self.profile)

        self.assertFalse(response.context['is_owner'])

    def test_profile_with_full_data_expect_correct_values(self):
        expected_values = {
            'username': 'foobar',
            'first_name': 'foo',
            'last_name': 'bar',
            'website': 'www.foo@bar.barz',
            'twitter': 'www.twitter.com/foobar',
            'instagram': 'www.instagram.com/foobar',
            'facebook': 'www.facebook.com/foobar'
        }

        response = self.__get_response_for_profile(self.profile)

        self.assertEqual(expected_values['username'],
                         response.context['profile'].user.username)  # can check for slug too
        self.assertEqual(expected_values['first_name'], response.context['profile'].first_name)
        self.assertEqual(expected_values['last_name'], response.context['profile'].last_name)
        self.assertEqual(expected_values['website'], response.context['profile'].website)
        self.assertEqual(expected_values['twitter'], response.context['profile'].twitter)
        self.assertEqual(expected_values['instagram'], response.context['profile'].instagram)
        self.assertEqual(expected_values['facebook'], response.context['profile'].facebook)

    def test_profile_with_none_data_expect_correct_values(self):
        self.profile.first_name = ''
        self.profile.facebook = ''
        self.profile.save()
        response = self.__get_response_for_profile(self.profile)

        self.assertFalse(response.context['profile'].first_name)
        self.assertFalse(response.context['profile'].facebook)
