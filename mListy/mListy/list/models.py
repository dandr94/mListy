from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

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
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    class Meta:
        unique_together = (('title', 'user'),)

    def __str__(self):
        return self.title
