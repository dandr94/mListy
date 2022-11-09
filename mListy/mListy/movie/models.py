from django.db import models


class MovieDB(models.Model):
    MOVIE_NAME_MAX_CHAR = 100
    GENRES_MAX_CHAR = 100
    ACTORS_MAX_CHAR = 1000
    ROLES_MAX_CHAR = 1000
    PRODUCTION_COMPANIES_MAX_CHAR = 1000
    LANGUAGE_MAX_CHAR = 10
    STATUS_MAX_CHAR = 100

    movie_id = models.IntegerField(
        unique=True
    )

    name = models.CharField(
        max_length=MOVIE_NAME_MAX_CHAR
    )

    poster = models.URLField(

    )

    description = models.TextField(

    )

    duration = models.IntegerField(

    )

    genres = models.CharField(
        max_length=GENRES_MAX_CHAR
    )

    average_grade = models.FloatField(

    )

    actors = models.CharField(
        max_length=ACTORS_MAX_CHAR
    )

    roles = models.CharField(
        max_length=ROLES_MAX_CHAR
    )

    production_companies = models.CharField(
        max_length=PRODUCTION_COMPANIES_MAX_CHAR
    )

    language = models.CharField(
        max_length=LANGUAGE_MAX_CHAR
    )

    imdb_link = models.URLField(

    )

    budget = models.FloatField(

    )

    release_date = models.DateField(

    )

    status = models.CharField(
        max_length=STATUS_MAX_CHAR
    )

    date_added = models.DateField(
        auto_now_add=True
    )

    last_updated = models.DateField(
        auto_now=True
    )

    def __str__(self):
        return self.name
