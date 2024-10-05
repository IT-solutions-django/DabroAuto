from django.core.management.base import BaseCommand, CommandError

from business.review_parser_2gis import UpdateReviewError
from business.update_review import update_review


class Command(BaseCommand):
    """
    Команда для обновления записей отзывов.
    """

    def handle(self, *args, **options):
        try:
            update_review()
        except UpdateReviewError as e:
            print(str(e))
            raise CommandError("Error when reviews updated. There are old data left.")
        except Exception:
            print("Произошла неизвестная ошибка при обновлении отзывов")
            raise CommandError("Error when reviews updated. There are old data left.")
        self.stdout.write(self.style.SUCCESS("Reviews Updated"))
