from django.core.management.base import BaseCommand

from tasks.tasks import update_currency_rate_task


class Command(BaseCommand):
    """
    Команда для обновления валют.
    """

    def handle(self, *args, **options):
        update_currency_rate_task.delay()

        self.stdout.write(self.style.SUCCESS("Currency rate Updating task started"))
