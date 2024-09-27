from django.db import models

from src.utils.model_mixins import NameMixin, ContentMixin, URLMixin


class SocialMedia(NameMixin, URLMixin):
    """Модель описывающая социальные сети автосалона"""

    class Meta:
        verbose_name = "социальная сеть"
        verbose_name_plural = "социальные сети"


class ContactInformation(NameMixin, ContentMixin):
    """Модель описывающая контактную информацию автосалона"""

    class Meta:
        verbose_name = "контактная информация"
        verbose_name_plural = "контактная информация"


class StagesOfWork(NameMixin, ContentMixin):
    """Модель описывающая этапы работы автосалона"""

    class Meta:
        verbose_name = "этап работы"
        verbose_name_plural = "этапы работы"


class InformationAboutCompany(ContentMixin):
    """Модель описывающая информацию об автосалоне"""

    block = models.CharField(
        max_length=255, help_text="максимальная длина 255 символов", verbose_name="блок"
    )

    def __str__(self):
        return self.block

    class Meta:
        verbose_name = "информация об автосалоне"
        verbose_name_plural = "информация об автосалоне"