from mListy.movie.tests.BaseMovieTest import BaseMovieTest
from mListy.movie.tests.utils import VALID_LIST_ENTRY_DATA


class AddListEntryFormTests(BaseMovieTest):
    PATH = 'add entry'
    EXPECTED_EMPTY_FIELD_ERROR_MSG = 'This field is required.'

    INVALID_GRADE_FIELD_DATA = {
        'grade': '',
        'list': 'Drama',
        'would_recommend': 'Yes'
    }

    INVALID_LIST_FIELD_DATA = {
        'grade': 5,
        'list': '',
        'would_recommend': 'Yes'
    }

    def setUp(self):
        super().setUp()
        self.path = self.get_path(self.PATH, {'slug': self.movie.slug})

    def test_empty_grade_field__should_return_correct_error_msg(self):
        field_name_key = 'grade'

        response = self.return_post_response(self.INVALID_GRADE_FIELD_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EXPECTED_EMPTY_FIELD_ERROR_MSG)

    def test_empty_list_field__should_return_correct_error_msg(self):
        field_name_key = 'list'

        response = self.return_post_response(self.INVALID_LIST_FIELD_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EXPECTED_EMPTY_FIELD_ERROR_MSG)

    def test_add_entry_in_a_list_with_existing_identical_entry__expect_correct_error_msg(self):
        VALID_LIST_ENTRY_DATA['list'] = self.list.id
        VALID_LIST_ENTRY_DATA['movie'] = self.movie
        response = self.return_post_response(VALID_LIST_ENTRY_DATA)
        expected_unique_list_entry_error_msg = f'{self.movie.name} is already in {self.list.title}.'
        self.assertFormError(response, self.FORM, None, expected_unique_list_entry_error_msg)


