from typing import List
import tmdbsimple as tmdb
from mListy.movie.helpers import MovieBlueprint


def return_last_added_entries(entries: list) -> List[object]:
    last_added = sorted(entries, key=lambda x: x.date_created, reverse=True)[:5]

    return last_added


def return_total_average_grade(entries: list) -> int:
    total_average_grade = sum(e.grade for e in entries) / len(entries) if entries else 0

    return total_average_grade


def return_trending_movies() -> List[MovieBlueprint]:
    trending = tmdb.Trending(media_type='movie', time_window='week')

    res = []

    for movie in trending.info()['results'][0:12]:
        res.append(MovieBlueprint(movie['id'], movie['title'], movie['poster_path'], movie['vote_average']))

    return res
