from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.model_mixins import NameMixin, ContentMixin, UpdatedAtMixin


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


class CountryRelatedMixin(models.Model):
    """Mixin для добавления связи с таблицей Country"""

    country_manufacturing = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        verbose_name="страна производства",
    )

    class Meta:
        abstract = True


class BaseFilter(CountryRelatedMixin):

    auction = models.CharField(
        max_length=20,
        verbose_name="название аукциона",
        help_text="исключаем аукционы содержащие эту часть в названии",
    )
    marka_name = ArrayField(
        models.CharField(max_length=20),
        verbose_name="марки автомобиля",
        help_text="исключаем эти марки",
        blank=True,
        null=True,
    )
    year = models.PositiveIntegerField(
        verbose_name="год выпуска",
        help_text="минимальный год для выборки",
    )
    eng_v = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="объем двигателя",
        help_text="строго больше какого значения (л)",
    )
    mileage = models.PositiveIntegerField(
        verbose_name="пробег",
        help_text="меньше или равен какому значению",
    )
    status = models.CharField(
        max_length=50,
        verbose_name="статус",
        help_text="строго равен значению",
        blank=True,
        null=True,
    )
    priv = ArrayField(
        models.CharField(max_length=20),
        verbose_name="привод автомобиля",
        help_text="исключаем эти приводы",
        blank=True,
        null=True,
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
    auction_date = models.PositiveIntegerField(
        verbose_name="дата аукциона",
        help_text="за какой период от текущей даты (дней)",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "базовый фильтр"
        verbose_name_plural = "базовые фильтры"

    def __str__(self):
        return self.country_manufacturing.name


class CarMark(CountryRelatedMixin):
    name = models.CharField(
        max_length=255,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "марка автомобиля"
        verbose_name_plural = "марки автомобиля"
        unique_together = ("name", "country_manufacturing")


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
        unique_together = ("name", "mark")


class CarColor(NameMixin):
    class Meta:
        verbose_name = "цвет автомобиля"
        verbose_name_plural = "цвета автомобиля"


class CarColorTag(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )
    color = models.ForeignKey(
        CarColor, on_delete=models.CASCADE, related_name="tags", verbose_name="цвет"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тег цвета автомобиля"
        verbose_name_plural = "теги цвета автомобиля"
        unique_together = ("name", "color")


class CurrencyRate(NameMixin, UpdatedAtMixin):
    course = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name="курс",
        help_text="стоимость одной единицы в рублях",
    )

    class Meta:
        verbose_name = "курс валют"
        verbose_name_plural = "курсы валют"
