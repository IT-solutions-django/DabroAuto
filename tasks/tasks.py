from celery import shared_task

from business.download_clips import download_clips
from business.parse_currency_rate import update_currency_rate
from business.sending_mail import send_email
from business.update_clip import update_clip
from business.update_review import update_review


@shared_task
def download_clips_task():
    download_clips()


@shared_task
def update_reviews_task():
    update_review()


@shared_task
def update_clips_task():
    update_clip()


@shared_task
def send_email_task(title: str, message: str):
    send_email(title, message)


@shared_task
def update_currency_rate_task():
    update_currency_rate()
