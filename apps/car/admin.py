from django.contrib import admin

from apps.car.models import (
    CountryManufacturing,
    CarBrand,
    CarModel,
    EngineType,
    Car,
    CarKPP,
    CarPriv,
)


@admin.register(CountryManufacturing)
class CountryManufacturingAdmin(admin.ModelAdmin):
    """Класс админ-панели страны создания автомобиля"""

    search_fields = ("name",)


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    """Класс админ-панели марки автомобиля"""

    search_fields = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    """Класс админ-панели модели автомобиля"""

    search_fields = ("name",)


@admin.register(CarKPP)
class CarKPPAdmin(admin.ModelAdmin):
    """Класс админ-панели КПП автомобиля"""

    search_fields = ("name",)


@admin.register(CarPriv)
class CarPrivAdmin(admin.ModelAdmin):
    """Класс админ-панели привода автомобиля"""

    search_fields = ("name",)


@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    """Класс админ-панели типа двигателя автомобиля"""

    search_fields = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Класс админ-панели автомобиля"""

    fields = (
        "brand",
        "model",
        "specification",
        "year_manufactured",
        "mileage",
        "engine_type",
        "country_manufacturing",
        "price",
        "is_popular",
        "kuzov",
        "kpp",
        "eng_v",
        "priv",
        "color",
        "image",
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
