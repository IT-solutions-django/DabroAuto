from typing import Any

from django.conf import settings
from django.db import transaction

from src.apps.clip.models import Clip
from src.apps.service_info.models import Settings
from src.business.youtube_integration import YouTubeClipParser


@transaction.atomic
def update_clip() -> None:
    """
    Обновление клипов. Парсинг из YouTube API и загрузка в базу.
    """
    playlist_url = "https://www.youtube.com/watch?v=VfSC0PJyMrY&list=PLD59-zQ-GT2g1don616MMZ5bZKD3rDMmJ"
    count_clips = 20

    new_clips_data = YouTubeClipParser(settings.YOUTUBE_API_KEY).get_clips_info(
        playlist_url, count_clips
    )

    _delete_old_data()

    _create_clips(new_clips_data)


def get_playlists_info() -> None:
    playlists_info = YouTubeClipParser(settings.YOUTUBE_API_KEY).get_playlists_info(
        "https://www.youtube.com/@batareyka25"
    )
    print(*playlists_info, sep="\n")


def _delete_old_data() -> None:
    """
    Удаление старых данных из таблицы Clip.
    """

    Clip.objects.all().delete()


def _create_clips(new_data: list[dict[str, Any]]) -> None:
    """
    Создание записей в БД о клипах.
    :param new_data: Данные для создания.
    """

    for clip in new_data:
        Clip.objects.create(
            name=clip["title"],
            url=clip["url"],
            youtube_id=clip["id"],
            thumbnail_url=clip["thumbnail_url"],
            view_count=clip["view_count"],
        )
