from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.utils.model_mixins import CreatedAtMixin, NameMixin, URLMixin


class ReviewLocation(NameMixin, URLMixin):
    """Модель описывающая площадку на которой расположен отзыв оставленный автосалону"""

    class Meta:
        verbose_name = "площадка с отзывом"
        verbose_name_plural = "площадки с отзывом"


class ReviewAuthor(models.Model):
    """Модель описывающая автора отзыва оставленного автосалону"""

    first_name = models.CharField(
        max_length=100,
        help_text="максимальная длина 100 символов",
        verbose_name="имя автора",
    )
    last_name = models.CharField(
        max_length=100,
        help_text="максимальная длина 100 символов",
        verbose_name="фамилия автора",
    )
    avatar_url = models.TextField(
        null=True,
        blank=True,
        help_text="ссылка в формате http/...",
        verbose_name="ссылка на аватарку",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "автор отзыва"
        verbose_name_plural = "авторы отзывов"


class Review(CreatedAtMixin):
    """Модель описывающая отзыв оставленный автосалону"""

    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="звезд",
        help_text="значение от 1 до 5",
    )
    author = models.OneToOneField(
        ReviewAuthor,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="автор",
    )
    location = models.ForeignKey(
        ReviewLocation,
        on_delete=models.PROTECT,
        related_name="review",
        verbose_name="площадка на которой расположен",
    )

    def __str__(self):
        return f"{self.stars} звезды от {self.author}"

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
