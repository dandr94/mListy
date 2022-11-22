from mListy.movie.tests.BaseMovieTest import BaseMovieTest


class EditListEntryFormTests(BaseMovieTest):
    PATH = 'edit entry'
    EMPTY_FIELD_ERROR_MSG = 'This field is required.'

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
        self.path = self.get_path(self.PATH, {'pk': self.entry.pk, 'slug': self.entry.slug})

    def test_empty_grade_field__should_return_correct_error_msg(self):
        field_name_key = 'grade'

        response = self.return_post_response(self.INVALID_GRADE_FIELD_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)

    def test_empty_list_field__should_return_correct_error_msg(self):
        field_name_key = 'list'

        response = self.return_post_response(self.INVALID_LIST_FIELD_DATA)
        self.assertFormError(response, self.FORM, field_name_key, self.EMPTY_FIELD_ERROR_MSG)
