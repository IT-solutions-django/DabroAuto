from typing import Any, Iterable

import googleapiclient.discovery

from urllib.parse import urlparse, parse_qs


class YouTubeClipParser:
    """
    Класс для взаимодействия с YouTube API
    Предназначен для получения информации о видеозаписях определенного плейлиста.
    """

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self, api_key: str) -> None:
        """
        Инициализация класса.
        :param api_key: developerKey получается на этой странице: https://console.cloud.google.com/apis/library/youtube.googleapis.com?project=linen-centaur.
        """

        self.youtube_client = googleapiclient.discovery.build(
            self.API_SERVICE_NAME, self.API_VERSION, developerKey=api_key
        )

    def get_clips_info(self, url: str, count_videos: int = 10) -> list[dict[str, Any]]:
        """
        Получение полной информации о клипах определенного плейлиста.
        :param url: Ссылка на плейлист. Пример: https://www.youtube.com/watch?v=VfSC0PJyMrY&list=PLD59-zQ-GT2g1don616MMZ5bZKD3rDMmJ.
        :param count_videos: Количество загружаемых видео.
        """

        playlist_id = self._get_playlist_id_by_url(url)
        videos_ids = self._get_playlist_videos_ids(playlist_id, count_videos)
        videos_info = self._get_videos_info_by_ids(videos_ids)
        return videos_info

    @staticmethod
    def _get_playlist_id_by_url(url: str) -> str:
        """
        Получение из ссылки на плейлист его id.
        :param url: Ссылка на плейлист.
        """

        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query)["list"][0]

    def _get_playlist_videos_ids(
        self, playlist_id: str, count_videos: int = 10
    ) -> list[str]:
        """
        Получаем id видеозаписей переданного плейлиста.
        :param playlist_id: id Плейлиста;
        :param count_videos: Количество загружаемых видео.
        """

        videos_short_info = (
            self.youtube_client.playlistItems()
            .list(
                part="contentDetails",
                maxResults=count_videos,
                playlistId=playlist_id,
            )
            .execute()
        )
        videos_ids = [
            video_short_info_item["contentDetails"]["videoId"]
            for video_short_info_item in videos_short_info["items"]
        ]
        return videos_ids

    def _get_videos_info_by_ids(
        self, videos_ids: Iterable[str]
    ) -> list[dict[str, Any]]:
        """
        Получаем необходимую информацию о видео по их id.
        :param videos_ids: Id видеозаписей.
        """

        videos_full_info = (
            self.youtube_client.videos()
            .list(
                part="snippet,contentDetails,statistics",
                id=",".join(videos_ids),
            )
            .execute()
        )

        videos_needed_info = [
            {
                "id": video_info["id"],
                "title": video_info["snippet"]["title"],
                "thumbnail_url": video_info["snippet"]["thumbnails"]["maxres"]["url"],
                "view_count": video_info["statistics"]["viewCount"],
                "url": f'https://www.youtube.com/watch?v={video_info["id"]}',
            }
            for video_info in videos_full_info["items"]
        ]

        return videos_needed_info
