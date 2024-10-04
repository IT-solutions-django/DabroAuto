from django.contrib import admin

from src.apps.catalog.models import BaseFilter


# Register your models here.


@admin.register(BaseFilter)
class BaseFilterAdmin(admin.ModelAdmin):
    fields = ("name", "model_name", "content")
