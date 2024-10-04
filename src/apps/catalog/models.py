from django.db import models

from src.utils.model_mixins import NameMixin, ContentMixin


class BaseFilter(NameMixin, ContentMixin):
    model_name = models.CharField(
        max_length=255, verbose_name="название поля фильтрации"
    )

    class Meta:
        verbose_name = "базовый фильтр"
        verbose_name_plural = "базовые фильтры"


class CarMark(NameMixin):
    class Meta:
        verbose_name = "марка автомобиля"
        verbose_name_plural = "марки автомобиля"


class CarModel(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )

    mark = models.ForeignKey(
        CarMark, on_delete=models.CASCADE, related_name="model", verbose_name="марка"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "модель автомобиля"
        verbose_name_plural = "модели автомобиля"


class CarColor(NameMixin):
    class Meta:
        verbose_name = "цвет автомобиля"
        verbose_name_plural = "цвета автомобиля"
