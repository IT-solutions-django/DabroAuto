from django.core.management.base import BaseCommand, CommandError

from tasks.tasks import update_clips_task


class Command(BaseCommand):
    """
    Команда для обновления записей клипов.
    """

    def handle(self, *args, **options):
        update_clips_task.delay()

        self.stdout.write(self.style.SUCCESS("Clips Updating task started"))
