from mListy.list_entry.tests.BaseListEntryTestClass import BaseListEntryTestClass


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


