from django.core.management.base import BaseCommand

from tasks.tasks import telegram_chats_update_task


class Command(BaseCommand):
    """
    Команда для обновления подключенных telegram чатов.
    """

    def handle(self, *args, **options):
        telegram_chats_update_task.delay()

        self.stdout.write(self.style.SUCCESS("Telegram chats Updating task started"))
