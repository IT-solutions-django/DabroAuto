import json

from django.core.management.base import BaseCommand, CommandError

from apps.car.models import Car, CarBrand, CarModel, EngineType, CountryManufacturing


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
                Car.objects.get_or_create(
                    specification=car_data["specification"],
                    year_manufactured=car_data["year_manufactured"],
                    mileage=car_data["mileage"],
                    price=car_data["price"],
                    brand=brand,
                    model=model,
                    engine_type=engine_type,
                    country_manufacturing=country_manufacturing,
                )

        except Exception as e:
            raise CommandError(e)
        else:
            self.stdout.write(self.style.SUCCESS("Cars Downloading success"))
