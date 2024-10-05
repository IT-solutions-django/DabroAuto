from django.core.management.base import BaseCommand

from tasks.tasks import download_clips_task


class Command(BaseCommand):
    """
    Команда для скачивания клипов.
    """

    def handle(self, *args, **options):
        download_clips_task.delay()

        self.stdout.write(self.style.SUCCESS("Clips Downloading task started"))
