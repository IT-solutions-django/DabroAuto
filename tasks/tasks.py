from celery import shared_task

from business.download_clips import download_clips
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
