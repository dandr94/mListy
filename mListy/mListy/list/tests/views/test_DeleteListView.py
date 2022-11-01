from django.contrib.auth import get_user_model
from django.test import TestCase
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS

from mListy.account.models import Profile
from mListy.list.models import List

UserModel = get_user_model()


class CreateListFormTests(TestCase):
    VALID_LIST_DATA = {
        'title': 'Drama'
    }
    DELETE_LIST_TEMPLATE = 'list/delete_list.html'

    VALID_TITLE_NAME = 'Drama'

    PATH = '/list/delete/'
    FORM = 'form'

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.list = List(title=self.VALID_TITLE_NAME, user=self.user)
        self.list.save()

    def __get_post_response(self, credentials):
        return self.client.post(self.PATH + self.list.slug + '/', args=credentials)

    def __get_get_response(self):
        return self.client.get(self.PATH + self.list.slug + '/')

    def test_correct_template_is_used(self):
        response = self.__get_get_response()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.DELETE_LIST_TEMPLATE)

    def test_delete_list(self):
        response = self.__get_post_response(self.list.id)

        user_list = List.objects.exists()

        self.assertFalse(user_list)

    def test_redirect_after_deletion(self):
        response = self.__get_post_response(self.list.id)

        expected_redirect_url = '/dashboard/'

        self.assertRedirects(response, expected_redirect_url)