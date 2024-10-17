import json

from django.core.management.base import BaseCommand, CommandError

from apps.car.models import (
    Car,
    CarBrand,
    CarModel,
    EngineType,
    CountryManufacturing,
    CarKPP,
    CarPriv,
)
from apps.catalog.models import CarColor, Country


class Command(BaseCommand):
    """
    Команда для скачивания цветов.
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        try:
            with open(options["file_path"], "r", encoding="utf-8") as file:
                cars_data = json.load(file)

            for car_data in cars_data:
                brand, _ = CarBrand.objects.get_or_create(name=car_data["brand"])
                model, _ = CarModel.objects.get_or_create(name=car_data["model"])
                engine_type, _ = EngineType.objects.get_or_create(
                    name=car_data["engine_type"]
                )
                country_manufacturing, _ = CountryManufacturing.objects.get_or_create(
                    name=car_data["country_manufacturing"]
                )
                color, _ = CarColor.objects.get_or_create(
                    name="Зеленый",
                    country_manufacturing=Country.objects.get(name="Япония"),
                )
                kpp, _ = CarKPP.objects.get_or_create(name=car_data["kpp"])
                priv, _ = CarPriv.objects.get_or_create(name=car_data["priv"])
                Car.objects.get_or_create(
                    specification=car_data["specification"],
                    year_manufactured=car_data["year_manufactured"],
                    mileage=car_data["mileage"],
                    price=car_data["price"],
                    brand=brand,
                    model=model,
                    engine_type=engine_type,
                    is_popular=car_data["is_popular"],
                    kuzov=car_data["kuzov"],
                    kpp=kpp,
                    eng_v=car_data["eng_v"],
                    priv=priv,
                    color=color,
                    country_manufacturing=country_manufacturing,
                )

        except Exception as e:
            raise CommandError(e)
        else:
            self.stdout.write(self.style.SUCCESS("Cars Downloading success"))
