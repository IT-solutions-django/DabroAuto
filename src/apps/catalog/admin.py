from django.contrib import admin

from src.apps.catalog.models import BaseFilter, CarMark, CarModel


# Register your models here.


@admin.register(BaseFilter)
class BaseFilterAdmin(admin.ModelAdmin):
    fields = ("name", "model_name", "content")


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0


@admin.register(CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "mark")
    search_fields = ("name",)
