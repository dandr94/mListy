from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from mListy.account.tests.utils import VALID_LOGIN_CREDENTIALS, VALID_USER_CREDENTIALS
from mListy.account.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):
    VALID_FULL_NAME_DATA = {
        'first_name': 'foo',
        'last_name': 'bar'
    }

    VALID_SHORT_NAME_DATA = {
        'first_name': 'foo'
    }

    INVALID_NAME_DATA = {
        'name_with_symbol': 'foo!!!barz',
        'name_with_space': 'foo bar',
        'name_with_number': 'foo123bar'
    }

    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_FULL_NAME_DATA,
            user=user
        )

        return user, profile

    # Profile first_name tests

    def test_profile_create__when_first_name_contains_only_letters_and_numbers__expect_success(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(self.VALID_FULL_NAME_DATA['first_name'], user=user)
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_symbol__expect_to_fail(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(first_name=self.INVALID_NAME_DATA['name_with_symbol'], user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(first_name=self.INVALID_NAME_DATA['name_with_space'], user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_number__expect_to_fail(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(first_name=self.INVALID_NAME_DATA['name_with_number'], user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)


    # Profile last_name tests

    def test_profile_create__when_last_name_contains_only_letters_and_numbers__expect_success(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(last_name=self.VALID_FULL_NAME_DATA['last_name'], user=user)
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_last_name_contains_a_symbol__expect_to_fail(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(last_name=self.INVALID_NAME_DATA['name_with_symbol'], user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_a_space__expect_to_fail(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(last_name=self.INVALID_NAME_DATA['name_with_space'], user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_a_number__expect_to_fail(self):
        user = self.__create_user(**VALID_USER_CREDENTIALS)
        profile = Profile(first_name=self.INVALID_NAME_DATA['name_with_number'], user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    # Profile full_name function test

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(**self.VALID_FULL_NAME_DATA)

        expected_full_name = f'{self.VALID_FULL_NAME_DATA["first_name"]} {self.VALID_FULL_NAME_DATA["last_name"]}'

        self.assertEqual(expected_full_name, profile.get_full_name())

    # Profile short_name function test

    def test_profile_short_name__when_valid__expect_correct_short_name(self):
        profile = Profile(**self.VALID_SHORT_NAME_DATA)

        expected_full_name = f'{self.VALID_SHORT_NAME_DATA["first_name"]}'

        self.assertEqual(expected_full_name, profile.get_short_name())
