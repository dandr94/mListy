from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

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

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (('title', 'user'),)

    def __str__(self):
        return self.title
