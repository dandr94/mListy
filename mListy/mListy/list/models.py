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

    def save(self, *args, **kwargs):
        slug = slugify(self.title)

        if not self.slug:
            self.slug = slug
        elif self.slug != slug:
            self.slug = slug

        return super().save(*args, **kwargs)

    class Meta:
        unique_together = (('title', 'user'),)

    def __str__(self):
        return self.title


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

    date_created = models.DateField(
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
