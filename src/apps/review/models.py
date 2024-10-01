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

    name = models.CharField(
        max_length=255,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )

    avatar_url = models.TextField(
        null=True,
        blank=True,
        help_text="ссылка в формате http/...",
        verbose_name="ссылка на аватарку",
    )

    @property
    def logo_text(self) -> str:
        return "".join(name_word[0].upper() for name_word in self.name.split())

    @property
    def logo_background(self) -> str:
        return "#A84CA8"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "автор отзыва"
        verbose_name_plural = "авторы отзывов"


class Review(models.Model):
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
    created_at = models.DateField(
        verbose_name="дата добавления отзыва",
    )

    def __str__(self):
        return f"{self.stars} звезды от {self.author}"

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        ordering = ("-created_at",)
