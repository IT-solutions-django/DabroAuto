from django.db import models


class NameMixin(models.Model):
    """Mixin для добавления поля name (обязательное, уникальное)"""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class URLMixin(models.Model):
    """Mixin для добавления поля url"""

    url = models.TextField(verbose_name="ссылка", help_text="ссылка в формате http/...")

    class Meta:
        abstract = True


class ContentMixin(models.Model):
    """Mixin для добавления поля content"""

    content = models.TextField(verbose_name="контент")

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    """Mixin для добавления поля created_at"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    """Mixin для добавления поля updated_at"""

    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата обновления")

    class Meta:
        abstract = True
