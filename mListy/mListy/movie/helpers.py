from typing import List, Tuple

import requests
import tmdbsimple as tmdb
from django.core.exceptions import ObjectDoesNotExist

from mListy.movie.models import MovieDB
from mListy.settings import YOUTUBE_SEARCH_API_KEY

TMDB_IMG_PATH = 'https://image.tmdb.org/t/p/w500/'
IMDB_PATH = 'https://www.imdb.com/title/'
IMG_NOT_FOUND = 'https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png'
NOT_AVAILABLE = 'N/A'
YOUTUBE_SEARCH_PATH = 'https://www.googleapis.com/youtube/v3/search'
YOUTUBE_BASIC_PATH = 'https://www.youtube.com/watch?v='
YOUTUBE_ADDITIONAL_QUERY_SEARCH_WORD = 'trailer hd'
YOUTUBE_MAX_RESULT_PAGES = 1
YOUTUBE_SEARCH_TYPE = 'video'
YOUTUBE_API_KEY = YOUTUBE_SEARCH_API_KEY


def check_if_in_db(movie_id: int) -> object or bool:  # FIX
    try:
        movie = MovieDB.objects.get(movie_id=movie_id)
        return movie
    except ObjectDoesNotExist:
        return False


def add_movie_to_db(movie_id: int) -> None:
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


def return_youtube_trailer(movie_name: str, release_date: str) -> str:
    search_url: str = YOUTUBE_SEARCH_PATH
    basic_path: str = YOUTUBE_BASIC_PATH
    query_params: str = movie_name + " " + release_date + " " + YOUTUBE_ADDITIONAL_QUERY_SEARCH_WORD

    search_params = {
        'part': 'snippet',
        'q': query_params,
        'key': YOUTUBE_API_KEY,
        'maxResults': YOUTUBE_MAX_RESULT_PAGES,
        'type': YOUTUBE_SEARCH_TYPE,
        'definition': 'hd',
    }

    search_result = requests.get(search_url, params=search_params)

    try:
        json_result = search_result.json()['items']
        path = basic_path + json_result[0]['id']['videoId']
        return path
    except KeyError:
        return ''


def return_last_added_entries(entries: dict) -> List[Tuple[object, int]]:
    last_added = sorted(entries.items(), key=lambda x: x[0].date_created, reverse=True)[:5]

    return last_added


def return_total_average_grade(entries: dict) -> int:
    total_average_grade = sum(entries.values()) // len(entries) if entries else 0

    return total_average_grade
