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

    position = models.PositiveIntegerField(verbose_name="позиция этапа")

    class Meta:
        verbose_name = "этап работы"
        verbose_name_plural = "этапы работы"
        ordering = ("position",)


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


class Settings(models.Model):
    """Модель описывающая информацию об настройках сайта"""

    youtube_channel_url = models.TextField(
        verbose_name="ссылка на канал", help_text="ссылка в формате http/..."
    )
    youtube_count_videos = models.PositiveIntegerField(
        verbose_name="количество видео для скачивания", help_text="положительное число"
    )

    reviews_service_url = models.TextField(
        verbose_name="ссылка на 2ГИС организации", help_text="ссылка в формате http/..."
    )
    reviews_count = models.PositiveIntegerField(
        verbose_name="количество отзывов для скачивания",
        help_text="положительное число",
    )

    class Meta:
        verbose_name = "настройка сайта"
        verbose_name_plural = "настройки сайта"
