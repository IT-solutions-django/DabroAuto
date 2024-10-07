from django.core.management.base import BaseCommand, CommandError

from tasks.tasks import update_reviews_task


class Command(BaseCommand):
    """
    Команда для обновления записей отзывов.
    """

    def handle(self, *args, **options):
        update_reviews_task.delay()

        self.stdout.write(self.style.SUCCESS("Reviews Updating task started"))
