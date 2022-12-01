from mListy.list.models import List
from mListy.list_entry.models import ListEntry
from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass
from mListy.list_entry.tests.utils import VALID_LIST_ENTRY_DATA


class EditListEntryFormTests(BaseListEntryTestClass):
    PATH = 'edit entry'
    EMPTY_FIELD_ERROR_MSG = 'This field is required.'

    def setUp(self):
        super().setUp()
        self.entry = self.create_entry()

    def test_empty_grade_field__should_return_correct_error_msg(self):
        field_name_key = 'grade'

        self.FIELD_DATA['grade'] = ''

        response = self.post_response_for_list_entry(self.entry, self.FIELD_DATA)

        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)

    def test_empty_list_field__should_return_correct_error_msg(self):
        field_name_key = 'list'

        self.FIELD_DATA['list'] = ''

        response = self.post_response_for_list_entry(self.entry, self.FIELD_DATA)

        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)

    def test_empty_status_field__should_return_correct_error_msg(self):
        field_name_key = 'status'

        self.FIELD_DATA['status'] = ''

        response = self.post_response_for_list_entry(self.entry, self.FIELD_DATA)

        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)

    def test_adding_the_entry_to_another_list_with_existing_identical_entry__expect_correct_error_msg(self):
        mock_list = List.objects.create(title='Mock', user=self.user)
        mock_entry = ListEntry.objects.create(**VALID_LIST_ENTRY_DATA, movie=self.movie, list=mock_list)

        self.assertTrue(mock_entry.pk)

        self.FIELD_DATA['list'] = self.user_list.id

        response = self.post_response_for_list_entry(mock_entry, self.FIELD_DATA)

        expected_error_msg = f'{self.movie.name} is already in {self.user_list}.'

        self.assertFormError(response, self.FORM, None, expected_error_msg)
