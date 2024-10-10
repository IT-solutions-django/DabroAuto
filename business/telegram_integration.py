import requests

from apps.telegram_sender.models import Chat
from config import settings


def get_new_chat_ids():
    res = requests.get(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/getUpdates"
    ).json()

    for message in res["result"]:
        if message["message"]["text"] == "/start":
            Chat.objects.get_or_create(chat_id=message["message"]["chat"]["id"])


def telegram_send_mail_for_all(text: str):
    chats_ids = Chat.objects.all()

    for chat_id in chats_ids:
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/sendMessage?chat_id={chat_id}&text={text}"
        )
