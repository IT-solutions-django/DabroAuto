from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.model_mixins import NameMixin, ContentMixin


class Country(NameMixin):
    table_name = models.CharField(
        unique=True,
        max_length=20,
        verbose_name="название таблицы",
        help_text="максимальная длина - 20",
    )

    class Meta:
        verbose_name = "страна производства"
        verbose_name_plural = "страны производства"


class BaseFilter(models.Model):
    country_manufacturing = models.OneToOneField(
        Country,
        on_delete=models.PROTECT,
        related_name="base_filter",
        verbose_name="страна производства",
    )

    auction_date = models.PositiveIntegerField(
        verbose_name="дата аукциона",
        help_text="за какой период от текущей даты (дней)",
    )
    auction = models.CharField(
        max_length=20,
        verbose_name="название аукциона",
        help_text="исключаем аукционы содержащие эту часть в названии",
    )
    marka_name = ArrayField(
        models.CharField(max_length=20),
        verbose_name="марки автомобиля",
        help_text="исключаем эти марки",
    )
    year = models.PositiveIntegerField(
        verbose_name="год выпуска",
        help_text="минимальный год для выборки",
    )
    eng_v = models.PositiveIntegerField(
        verbose_name="объем двигателя",
        help_text="строго больше какого значения",
    )
    mileage = models.PositiveIntegerField(
        verbose_name="пробег",
        help_text="меньше или равен какому значению",
    )
    status = models.CharField(
        max_length=50,
        verbose_name="статус",
        help_text="строго равен значению",
    )
    finish = models.PositiveIntegerField(
        verbose_name="финиш",
        help_text="строго больше какого значения",
    )
    kpp_type = ArrayField(
        models.PositiveIntegerField(),
        verbose_name="типы КПП",
        help_text="исключаем эти типы",
    )

    class Meta:
        verbose_name = "базовый фильтр"
        verbose_name_plural = "базовые фильтры"

    def __str__(self):
        return self.country_manufacturing.name


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
