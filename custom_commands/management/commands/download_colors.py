import json

from django.core.management.base import BaseCommand, CommandError

from apps.catalog.models import CarColorTag, CarColor, Country


class Command(BaseCommand):
    """
    Команда для скачивания цветов.
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("country_id", type=int)

    def handle(self, *args, **options):
        try:
            with open(options["file_path"], "r", encoding="utf-8") as file:
                colors_data = json.load(file)

            country = Country.objects.get(id=options["country_id"])
            for color in colors_data:
                current_color, _ = CarColor.objects.get_or_create(
                    name=color["name"], country_manufacturing=country
                )
                for current_color_tag in color["colors"]:
                    CarColorTag.objects.get_or_create(
                        name=current_color_tag,
                        color=current_color,
                    )

        except Exception as e:
            raise CommandError(e)
        else:
            self.stdout.write(self.style.SUCCESS("Colors Downloading success"))
