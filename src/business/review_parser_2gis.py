from typing import Any

import requests


def get_2gis_organization_reviews_info(
    url: str, reviews_limit: int = 10
) -> dict[str, Any] | None:
    """
    Получаем информацию об отзывах определенной организации.
    :param reviews_limit: Количество отзывов в ответе (default: 10);
    :param url: Ссылка на организацию 2 gis (пример: https://2gis.ru/vladivostok/firm/70000001044743727/tab/reviews);
    :return: Словарь с данными об отзывах организации.
    """

    organization_id = _get_organization_id_by_url(url)
    try:
        fetched_reviews = _fetch_reviews(organization_id, reviews_limit)
    except requests.exceptions.RequestException:
        return None

    result = _get_needed_data_format(fetched_reviews)
    return result


def _get_organization_id_by_url(url: str) -> str:
    """
    Получаем Id организации по ссылке на нее из 2 gis.
    :param url: Ссылка на организацию 2 gis (пример: https://2gis.ru/vladivostok/firm/70000001044743727/tab/reviews);
    :return: Id организации 2 gis.
    """

    return url.split("/")[5]


def _fetch_reviews(organization_id: str, reviews_limit: int = 10) -> dict[str, dict]:
    """
    Использую публичное API 2gis, получаем полную информацию об отзывах организации.
    :param organization_id: Id организации 2gis;
    :param reviews_limit: Количество отзывов в ответе (default: 10);
    :return: Словарь ответа 2gis API.
    """

    # FIXME Обернуть в декоратор retry для нескольких попыток
    response = requests.get(
        f"https://public-api.reviews.2gis.com/2.0/branches/{organization_id}/reviews?"
        f"limit={reviews_limit}&is_advertiser=false&fields=meta.branch_rating&sort_by=date_edited&"
        f"key=b0209295-ae15-48b2-acb2-58309b333c37&locale=ru_RU"
    )
    return response.json()


def _get_needed_data_format(fetched_data: dict[str, dict]) -> dict[str, Any]:
    """
    Фильтрация ненужных данных ответа и преобразование нужных в необходимый формат.
    :param fetched_data: Данные ответа от API 2gis;
    :return: Словарь с данными об отзывах организации
    """

    return {
        "average_review": fetched_data["meta"]["branch_rating"],
        "reviews": [
            {
                "stars": review["rating"],
                "created_at": review["date_edited"] or review["date_created"],
                "author": {
                    "name": review["user"]["name"],
                    "avatar": review["user"]["photo_preview_urls"]["url"] or None,
                },
            }
            for review in fetched_data["reviews"]
        ],
    }
