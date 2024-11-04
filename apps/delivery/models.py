from django.utils.translation import gettext_lazy as _
from django.db import models


class City(models.Model):
    name = models.CharField(verbose_name=_("Название города"), max_length=100)
    time = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name='Время доставки в днях')

    class Meta:
        verbose_name = _("Города")
        verbose_name_plural = _("Город")

    def __str__(self):
        return f"{self.name}"


class DeliveryBody(models.Model):
    name = models.CharField(
        verbose_name=_("Кузов"), max_length=100
    )

    class Meta:
        verbose_name = _("Кузов")
        verbose_name_plural = _("Кузов")

    def __str__(self):
        return f"{self.name}"


class Delivery(models.Model):
    class Meta:
        verbose_name = _("Стоимость")
        verbose_name_plural = _("Стоимость")

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name=_("Город доставки")
    )

    body_type = models.ForeignKey(
        DeliveryBody, on_delete=models.CASCADE, verbose_name=_("Тип кузова")
    )

    price = models.IntegerField(verbose_name=_("Стоимость доставки"), default=0)

    def __str__(self):
        return f"{self.city} {self.body_type} {self.price}"
