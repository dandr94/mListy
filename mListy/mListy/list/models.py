from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from mListy.movie.models import MovieDB

UserModel = get_user_model()


class List(models.Model):
    LIST_TITLE_MAX_CHAR = 30
    LIST_TITLE_MIN_CHAR = 2

    title = models.CharField(
        max_length=LIST_TITLE_MAX_CHAR,
        validators=[MinLengthValidator(LIST_TITLE_MIN_CHAR)]
    )

    cover = models.URLField(
        blank=True,
        null=True,
        verbose_name='URL Field'

    )

    slug = models.SlugField(blank=True, null=True)

    date_created = models.DateTimeField(
        auto_now_add=True
    )

    last_updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    movie_list = models.ManyToManyField(MovieDB)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    class Meta:
        unique_together = (('title', 'user'),)

    def __str__(self):
        return self.title


class ListEntry(models.Model):
    MOVIE_NAME_MAX_CHAR = 50
    MOVIE_NAME_MIN_CHAR = 2

    GRADE_MAX_CHAR = 10
    GRADE_CHOICE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )
    WOULD_RECOMMEND_CHOICE = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('---', '---')
    ]

    RELEASE_DATE_MAX_CHAR = 15

    movie_id = models.IntegerField(

    )

    movie_name = models.CharField(
        max_length=MOVIE_NAME_MAX_CHAR,
        validators=[
            MinLengthValidator(MOVIE_NAME_MIN_CHAR)
        ]
    )

    slug = models.SlugField(blank=True, null=True)

    grade = models.IntegerField(
        choices=GRADE_CHOICE

    )

    would_recommend = models.CharField(
        max_length=15,
        choices=WOULD_RECOMMEND_CHOICE,
        default=WOULD_RECOMMEND_CHOICE[2],
    )

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )

    list = models.ForeignKey(
        List, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.movie_name)

        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('movie_id', 'list')

    def __str__(self):
        return f'{self.movie_name}'
