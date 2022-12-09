from django.urls import reverse
from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass


class AddListEntryFormTests(BaseListEntryTestClass):
    PATH = 'add entry'
    EMPTY_FIELD_ERROR_MSG = 'This field is required.'

    def __return_post_response_(self):
        return self.client.post(reverse(self.PATH, kwargs={'slug': self.movie.slug}), self.FIELD_DATA)

    def test_empty_grade_field__should_return_correct_error_msg(self):
        field_name_key = 'grade'

        self.FIELD_DATA['grade'] = ''

        response = self.__return_post_response_()

        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)

    def test_empty_list_field__should_return_correct_error_msg(self):
        field_name_key = 'list'

        self.FIELD_DATA['list'] = ''

        response = self.__return_post_response_()

        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)

    def test_empty_status_field__should_return_correct_error_msg(self):
        field_name_key = 'status'

        self.FIELD_DATA['status'] = ''

        response = self.__return_post_response_()

        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)

    def test_add_entry_in_a_list_with_existing_identical_entry__expect_correct_error_msg(self):
        self.create_entry()

        self.FIELD_DATA['list'] = self.user_list.id
        self.FIELD_DATA['movie'] = self.movie

        response = self.__return_post_response_()

        expected_unique_list_entry_error_msg = f'{self.movie.name} is already in {self.user_list.title}.'

        self.assertFormError(response, self.FORM, None, expected_unique_list_entry_error_msg)
