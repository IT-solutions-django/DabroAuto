from django.core.management.base import BaseCommand

from tasks.tasks import update_catalog_meta_task


class Command(BaseCommand):
    """
    Команда для выгрузки данных для таблиц справочников.
    """

    def handle(self, *args, **options):
        update_catalog_meta_task.delay()

        self.stdout.write(self.style.SUCCESS("Catalog meta Downloaded"))
