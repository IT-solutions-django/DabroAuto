from django.core.management.base import BaseCommand, CommandError

from business.update_clip import update_clip


class Command(BaseCommand):
    """
    Команда для обновления записей клипов.
    """

    def handle(self, *args, **options):
        try:
            update_clip()
        except Exception:
            raise CommandError("Error when clips updated. There are old data left.")

        self.stdout.write(self.style.SUCCESS("Clips Updated"))
