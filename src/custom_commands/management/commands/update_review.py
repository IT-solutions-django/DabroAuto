from django.core.management.base import BaseCommand, CommandError

from src.business.update_review import update_review, send_error_message


class Command(BaseCommand):
    """
    Команда для обновления записей отзывов.
    """

    def handle(self, *args, **options):
        try:
            update_review()
        except Exception:
            send_error_message()
            raise CommandError("Error when reviews updated. There are old data left.")

        self.stdout.write(self.style.SUCCESS("Reviews Updated"))
