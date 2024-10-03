from django.core.mail import send_mail

from src.config import settings


def send_email(title: str, message: str):
    send_mail(
        title, message, settings.EMAIL_HOST_USER, [settings.EMAIL_TO_GETTING_INFO]
    )
