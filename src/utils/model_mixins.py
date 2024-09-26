from django.db import models


class NamingMixin(models.Model):
    """Mixin для добавления поля name (обязательное, уникальное)"""

    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    class Meta:
        abstract = True


class URLMixin(models.Model):
    """Mixin для добавления поля url"""

    url = models.TextField(verbose_name="ссылка")

    class Meta:
        abstract = True


class ContentMixin(models.Model):
    """Mixin для добавления поля content"""

    content = models.TextField(verbose_name="контент")

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    """Mixin для добавления поля created_at"""

    created_at = models.DateTimeField(auto_now=True, verbose_name="дата создания")

    class Meta:
        abstract = True
