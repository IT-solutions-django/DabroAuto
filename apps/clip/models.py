from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.model_mixins import NameMixin, URLMixin


class ClipPlatform(NameMixin, URLMixin):
    """Модель описывающая платформу, где хранятся клипы"""

    playlists = ArrayField(
        models.CharField(max_length=20),
        verbose_name="плейлисты",
        help_text="плейлисты где расположены клипы, несколько значений разделяются запятой",
        blank=True,
        null=True,
    )

    count_upload = models.PositiveIntegerField(
        verbose_name="количество для скачивания", default=0, help_text="больше нуля"
    )

    class Meta:
        verbose_name = "площадка с клипами"
        verbose_name_plural = "площадки с клипами"


class Clip(NameMixin, URLMixin):
    """Модель описывающая YouTube клип"""

    youtube_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Id youtube",
        help_text="максимальная длина 255 символов",
    )

    thumbnail_url = models.TextField(
        verbose_name="ссылка на миниатюру", help_text="ссылка в формате http/..."
    )

    view_count = models.PositiveIntegerField(
        verbose_name="число просмотров", help_text="положительное число"
    )

    class Meta:
        verbose_name = "клип"
        verbose_name_plural = "клипы"
        ordering = ("id",)
