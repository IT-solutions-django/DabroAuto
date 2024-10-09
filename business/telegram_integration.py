import requests

from apps.telegram_sender.models import Chat


def get_new_chat_ids():
    res = requests.get(
        "https://api.telegram.org/bot7878060189:AAHpQeF6nv8Tls3a339jDcojuwIOui7kJy0/getUpdates"
    ).json()

    for message in res["result"]:
        if message["message"]["text"] == "/start":
            Chat.objects.get_or_create(chat_id=message["message"]["chat"]["id"])
