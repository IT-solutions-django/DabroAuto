from django.contrib import admin

from src.apps.car.models import (
    CountryManufacturing,
    CarBrand,
    CarModel,
    EngineType,
    Car,
)


@admin.register(CountryManufacturing)
class CountryManufacturingAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    fields = (
        "brand",
        "model",
        "specification",
        "year_manufactured",
        "mileage",
        "engine_type",
        "country_manufacturing",
        "price",
    )
    autocomplete_fields = (
        "brand",
        "model",
        "engine_type",
        "country_manufacturing",
    )
    search_fields = (
        "brand",
        "model",
        "specification",
        "year_manufactured",
    )
