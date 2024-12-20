from datetime import datetime
from typing import Any

from django.conf import settings
from django.db import transaction

from apps.review.models import Review, ReviewAuthor, ReviewLocation
from apps.service_info.models import InformationAboutCompany
from business.review_parser_2gis import (
    get_2gis_organization_reviews_info,
    UpdateReviewError,
)


@transaction.atomic
def update_review() -> None:
    """
    Обновление отзывов. Парсинг из 2gis и загрузка в базу.
    """
    review_location = _get_data_from_db(ReviewLocation, name="2ГИС")

    new_review_data = get_2gis_organization_reviews_info(
        review_location.url,
        settings.API_KEY_2GIS,
        review_location.count_upload,
    )

    _delete_old_data()

    _create_reviews(new_review_data["reviews"], review_location)
    _create_average_review(new_review_data["average_review"])


def _get_data_from_db(klass: Any, *args: Any, **kwargs: Any) -> Any:
    """
    Получение Данных из БД (get возвращающий кастомное исключение).
    """

    try:
        return klass.objects.get(*args, **kwargs)
    except Exception:
        raise UpdateReviewError("Не найдена соответствующая запись в БД")


def _delete_old_data() -> None:
    """
    Удаление старых данных из таблиц: Review, ReviewAuthor.
    """

    Review.objects.all().delete()
    ReviewAuthor.objects.all().delete()


def _create_reviews(reviews: list[dict], review_location: ReviewLocation) -> None:
    """
    Создание записей в БД об отзывах и их авторах.
    :param reviews: Данные для создания;
    :param review_location: Локация, где расположены отзывы (2gis).
    """

    for review in reviews:
        review_author = ReviewAuthor.objects.create(
            name=review["author"]["name"], avatar_url=review["author"]["avatar"]
        )
        Review.objects.create(
            stars=review["stars"],
            author=review_author,
            location=review_location,
            created_at=datetime.strptime(
                review["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
            ),
            text=review['text']
        )


def _create_average_review(average_review: float) -> None:
    """
    Обновление записи о средней оценке в БД.
    :param average_review: Средняя оценка.
    """

    InformationAboutCompany.objects.update_or_create(
        block="Средний рейтинг", defaults={"content": average_review}
    )
