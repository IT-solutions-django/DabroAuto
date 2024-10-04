from django.db import models

from src.utils.model_mixins import NameMixin, ContentMixin


class BaseFilter(NameMixin, ContentMixin):
    model_name = models.CharField(
        max_length=255, verbose_name="название поля фильтрации"
    )

    class Meta:
        verbose_name = "базовый фильтр"
        verbose_name_plural = "базовые фильтры"
