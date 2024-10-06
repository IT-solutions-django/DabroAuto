from django.core.validators import RegexValidator
from django.db import models

from utils.model_mixins import NameMixin, ContentMixin, URLMixin, CreatedAtMixin


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


class Questionnaire(CreatedAtMixin):
    """Модель описывающая информацию об обратной связи"""

    name = models.CharField(
        max_length=20,
        verbose_name="имя отправителя",
        help_text="максимальная длина 255 символов",
    )
    phone_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r"^\+7 \d{3} \d{3} \d{2} \d{2}$",
                message="Номер телефона должен быть определенного формата: '+7 999 999 99 99'.",
            )
        ],
        verbose_name="номер телефона",
        help_text="формат: '+79999999999'",
    )
    content = models.TextField(verbose_name="контент", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратная связь"
