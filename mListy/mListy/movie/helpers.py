from django.core.exceptions import ObjectDoesNotExist
import tmdbsimple as tmdb
from mListy.movie.models import MovieDB

TMDB_IMG_PATH = 'https://image.tmdb.org/t/p/w500/'
IMDB_PATH = 'https://www.imdb.com/title/'
IMG_NOT_FOUND = 'https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png'
NOT_AVAILABLE = 'N/A'


def check_if_in_db(movie_id: int) -> object:
    try:
        movie = MovieDB.objects.get(movie_id=movie_id)
        return movie
    except ObjectDoesNotExist:
        return False


def add_movie_to_db(movie_id: int):
    movie = tmdb.Movies(movie_id)
    info = movie.info()

    data = {
        'movie_id': movie_id,
        'name': info['title'],
        'poster': TMDB_IMG_PATH + info['poster_path'] if info['poster_path'] else IMG_NOT_FOUND,
        'description': info['overview'] if info['overview'] else NOT_AVAILABLE,
        'duration': info['runtime'] if info['runtime'] else 0,
        'genres': ", ".join([g['name'] for g in info['genres']]) if info['genres'] else NOT_AVAILABLE,
        'average_grade': info['vote_average'] if info['vote_average'] else 0,
        'actors': ", ".join([cast['name'] for cast in movie.credits()['cast'][:10]]) if movie.credits()[
            'cast'] else NOT_AVAILABLE,
        'roles': ", ".join([cast['character'] for cast in movie.credits()['cast'][:10]]) if movie.credits()[
            'cast'] else NOT_AVAILABLE,
        'production_companies': ", ".join([c['name'] for c in info['production_companies']]) if info[
            'production_companies'] else NOT_AVAILABLE,
        'language': info['original_language'].upper() if info['original_language'] else NOT_AVAILABLE,
        'imdb_link': IMDB_PATH + info['imdb_id'] if info['imdb_id'] else NOT_AVAILABLE,
        'budget': info['budget'],
        'release_date': info['release_date'],
        'status': info['status'] if info['status'] else NOT_AVAILABLE

    }

    MovieDB(**data).save()
