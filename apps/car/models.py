from django.db import models

from apps.catalog.models import CarColor
from apps.image.models import Image
from utils.model_mixins import NameMixin


class CountryManufacturing(NameMixin):
    """Модель описывающая страны производства автомобиля"""

    class Meta:
        verbose_name = "страна производства"
        verbose_name_plural = "страны производства"


class EngineType(NameMixin):
    """Модель описывающая тип двигателя автомобиля"""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тип двигателя"
        verbose_name_plural = "типы двигателя"


class CarBrand(NameMixin):
    """Модель описывающая марку автомобиля"""

    class Meta:
        verbose_name = "марка автомобиля"
        verbose_name_plural = "марки автомобиля"


class CarModel(NameMixin):
    """Модель описывающая модель автомобиля"""

    class Meta:
        verbose_name = "модель автомобиля"
        verbose_name_plural = "модели автомобиля"


class CarKPP(NameMixin):
    """Модель описывающая КПП автомобиля"""

    class Meta:
        verbose_name = "КПП автомобиля"
        verbose_name_plural = "КПП автомобиля"


class CarPriv(NameMixin):
    """Модель описывающая Привод автомобиля"""

    class Meta:
        verbose_name = "Привод автомобиля"
        verbose_name_plural = "Привод автомобиля"


class Car(models.Model):
    """Модель описывающая автомобиль"""

    specification = models.CharField(
        max_length=100,
        verbose_name="спецификация",
        help_text="максимальная длина - 100 символов",
    )
    year_manufactured = models.PositiveIntegerField(
        verbose_name="год выпуска", help_text="положительное число"
    )
    mileage = models.PositiveIntegerField(
        verbose_name="пробег", help_text="положительное число"
    )
    price = models.PositiveIntegerField(
        verbose_name="цена", help_text="положительное число"
    )

    brand = models.ForeignKey(
        CarBrand,
        on_delete=models.PROTECT,
        related_name="car",
        verbose_name="марка",
    )
    model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        related_name="car",
        verbose_name="модель",
    )
    engine_type = models.ForeignKey(
        EngineType,
        on_delete=models.PROTECT,
        related_name="car",
        verbose_name="тип двигателя",
    )
    country_manufacturing = models.ForeignKey(
        CountryManufacturing,
        on_delete=models.PROTECT,
        related_name="car",
        verbose_name="страна производства",
    )
    is_popular = models.BooleanField(
        default=False, verbose_name="показывать в популярных"
    )
    kuzov = models.CharField(
        max_length=100,
        verbose_name="кузов",
        help_text="максимальная длина - 100 символов",
    )
    kpp = models.ForeignKey(
        CarKPP,
        on_delete=models.PROTECT,
        related_name="car",
        verbose_name="КПП",
    )
    eng_v = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="объем двигателя",
        help_text="значение в литрах",
    )
    priv = models.ForeignKey(
        CarPriv,
        on_delete=models.PROTECT,
        related_name="car",
        verbose_name="привод",
    )
    color = models.ForeignKey(
        CarColor,
        on_delete=models.PROTECT,
        related_name="car",
        verbose_name="цвет",
    )
    image = models.ManyToManyField(
        Image, related_name="car", verbose_name="изображение"
    )

    @property
    def beautiful_price(self):
        return "{0:,}".format(self.price).replace(",", " ")

    @property
    def beautiful_mileage(self):
        return "{0:,}".format(self.mileage).replace(",", " ")

    @property
    def beautiful_eng_v(self):
        return str(self.eng_v).replace(",", ".")

    def __str__(self):
        return f"{self.brand} {self.model} {self.specification}"

    class Meta:
        verbose_name = "автомобиль"
        verbose_name_plural = "автомобили"
        ordering = ("-price",)
