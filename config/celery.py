import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_reviews": {
        "task": "tasks.tasks.update_reviews_task",
        "schedule": crontab(hour="4", minute="0"),
    },
    "update_clips": {
        "task": "tasks.tasks.update_clips_task",
        "schedule": crontab(hour="4", minute="1"),
    },
    "download_clips": {
        "task": "tasks.tasks.download_clips_task",
        "schedule": crontab(hour="4", minute="2"),
    },
    "update_currency_rate": {
        "task": "tasks.tasks.update_currency_rate_task",
        "schedule": crontab(hour="11", minute="0"),
    },
    "telegram_chats_update": {
        "task": "tasks.tasks.telegram_chats_update_task",
        "schedule": timedelta(hours=2),
    },
}
