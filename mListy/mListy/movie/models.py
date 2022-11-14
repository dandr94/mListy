from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


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
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    duration = models.IntegerField(
        blank=True,
        null=True
    )

    genres = models.CharField(
        blank=True,
        null=True,
        max_length=GENRES_MAX_CHAR
    )

    average_grade = models.FloatField(
        blank=True,
        null=True,
    )

    actors = models.CharField(
        blank=True,
        null=True,
        max_length=ACTORS_MAX_CHAR
    )

    roles = models.CharField(
        blank=True,
        null=True,
        max_length=ROLES_MAX_CHAR
    )

    production_companies = models.CharField(
        blank=True,
        null=True,
        max_length=PRODUCTION_COMPANIES_MAX_CHAR
    )

    language = models.CharField(
        blank=True,
        null=True,
        max_length=LANGUAGE_MAX_CHAR
    )

    imdb_link = models.URLField(
        blank=True,
        null=True,
    )

    budget = models.FloatField(
        blank=True,
        null=True,
    )

    release_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        blank=True,
        null=True,
        max_length=STATUS_MAX_CHAR
    )

    date_added = models.DateField(
        auto_now_add=True
    )

    last_updated = models.DateField(
        auto_now=True
    )

    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.movie_id) + '-' + self.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
