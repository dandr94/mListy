from django.contrib.auth import get_user_model
from django.test import TestCase

from mListy.account.models import Profile
from mListy.account.tests.utils import VALID_USER_CREDENTIALS, VALID_LOGIN_CREDENTIALS
from mListy.list.models import List

UserModel = get_user_model()


class CreateListViewTests(TestCase):
    PATH = '/list/edit/'
    EDIT_LIST_TEMPLATE = 'list/edit_list.html'

    VALID_LIST_DATA = {
        'title': 'Drama'
    }
    VALID_TITLE_NAME = 'Drama'
    MOCK_TITLE = 'Horror'
    MOCK_COVER = ''

    def setUp(self):
        self.user = UserModel.objects.create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.profile.save()
        self.client.login(**VALID_LOGIN_CREDENTIALS)
        self.list = List(title=self.VALID_TITLE_NAME, user=self.user)
        self.list.save()
        self.PATH += self.list.slug + '/'

    def test_correct_template_is_used(self):
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.EDIT_LIST_TEMPLATE)

    def test_edit_list_with_valid_credentials(self):

        response = self.client.get(self.PATH)
        form = response.context['form']
        data = form.initial

        self.assertContains(response, self.VALID_TITLE_NAME)

        data['title'] = self.MOCK_TITLE
        data['cover'] = self.MOCK_COVER

        response = self.client.post(self.PATH, data, follow=True)

        self.assertContains(response, self.MOCK_TITLE)

    def test_redirect_after_valid_edit(self):
        response = self.client.get(self.PATH)
        form = response.context['form']
        data = form.initial

        self.assertContains(response, self.VALID_TITLE_NAME)

        data['title'] = self.MOCK_TITLE
        data['cover'] = self.MOCK_COVER

        response = self.client.post(self.PATH, data)
        expected_url = '/dashboard/'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
