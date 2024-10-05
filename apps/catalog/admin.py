from django.contrib import admin

from apps.catalog.models import BaseFilter, CarMark, CarModel, CarColor


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


@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    search_fields = ("name",)
