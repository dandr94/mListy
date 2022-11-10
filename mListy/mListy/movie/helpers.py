from django.core.exceptions import ObjectDoesNotExist

from mListy.movie.models import MovieDB


def check_if_in_db(movie_id: int) -> object:
    try:
        movie = MovieDB.objects.get(movie_id=movie_id)
        return movie
    except ObjectDoesNotExist:
        return False

