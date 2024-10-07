from django.core.management.base import BaseCommand

from business.catalog_parser import update_catalog_meta


class Command(BaseCommand):
    """
    Команда для выгрузки данных для таблиц справочников.
    """

    def handle(self, *args, **options):
        update_catalog_meta()

        self.stdout.write(self.style.SUCCESS("Catalog meta Downloaded"))
