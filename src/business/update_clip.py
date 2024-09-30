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
    youtube_api_key = Settings.objects.get(
        name=settings.YOUTUBE_DEVELOPER_KEY_SETTINGS_NAME
    )
    playlist_url = Settings.objects.get(name=settings.PLAYLIST_URL_SETTINGS)
    count_clips = Settings.objects.get(name=settings.CLIPS_COUNT_SETTINGS)

    new_clips_data = YouTubeClipParser(youtube_api_key.content).get_clips_info(
        playlist_url.content, int(count_clips.content)
    )

    _delete_old_data()

    _create_clips(new_clips_data)


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
