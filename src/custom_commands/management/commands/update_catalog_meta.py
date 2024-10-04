from django.core.management.base import BaseCommand, CommandError

from src.business.catalog_filtering import construct_query_with_base_filters


class Command(BaseCommand):
    """
    Команда для выгрузки данных для таблиц справочников.
    """

    def handle(self, *args, **options):
        try:
            construct_query_with_base_filters()
        except Exception:
            raise CommandError("Error when clips download. There are old data left.")

        self.stdout.write(self.style.SUCCESS("Clips Downloaded"))
