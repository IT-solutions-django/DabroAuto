from django.db import models

from src.utils.model_mixins import NameMixin, URLMixin


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
