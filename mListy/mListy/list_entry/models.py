from django.db import models
from django.utils.text import slugify

from mListy.list.models import List
from mListy.movie.models import MovieDB


class ListEntry(models.Model):
    GRADE_MAX_CHAR = 10
    SLUG_MAX_CHAR = 255

    CHOICES_MAX_CHAR = 15

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

    WOULD_RECOMMEND_VERBOSE = 'Would Recommend'

    STATUS_CHOICE = [
        ('Completed', 'Completed'),
        ('Watching', 'Watching'),
        ('Dropped', 'Dropped')
    ]

    RELEASE_DATE_MAX_CHAR = 15

    slug = models.SlugField(
        max_length=SLUG_MAX_CHAR,
        blank=True,
        null=True
    )

    grade = models.IntegerField(
        choices=GRADE_CHOICE

    )

    would_recommend = models.CharField(
        max_length=CHOICES_MAX_CHAR,
        choices=WOULD_RECOMMEND_CHOICE,
        default=WOULD_RECOMMEND_CHOICE[2],
        verbose_name=WOULD_RECOMMEND_VERBOSE
    )

    status = models.CharField(
        max_length=CHOICES_MAX_CHAR,
        choices=STATUS_CHOICE,
    )

    date_created = models.DateTimeField(
        auto_now_add=True
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    movie = models.ForeignKey(
        MovieDB, on_delete=models.CASCADE
    )

    list = models.ForeignKey(
        List, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.movie.movie_id) + '-' + self.movie.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.movie.name
