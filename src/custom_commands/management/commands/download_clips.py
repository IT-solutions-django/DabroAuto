from django.core.management.base import BaseCommand, CommandError

from src.business.download_clips import download_clips
from src.business.update_clip import update_clip


class Command(BaseCommand):
    """
    Команда для скачивания клипов.
    """

    def handle(self, *args, **options):
        try:
            download_clips()
        except Exception:
            raise CommandError("Error when clips download. There are old data left.")

        self.stdout.write(self.style.SUCCESS("Clips Downloaded"))
