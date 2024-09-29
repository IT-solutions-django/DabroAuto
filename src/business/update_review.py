from datetime import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404

from src.apps.review.models import Review, ReviewAuthor, ReviewLocation
from src.apps.service_info.models import InformationAboutCompany
from src.business.review_parser_2gis import (
    get_2gis_organization_reviews_info,
)

REVIEWS_LOCATION_NAME = "2gis"
COUNT_REVIEWS = 20


@transaction.atomic
def update_review() -> None:
    """
    Обновление отзывов. Парсинг из 2gis и загрузка в базу.
    """

    review_location = _get_review_location_to_parse(REVIEWS_LOCATION_NAME)
    new_review_data = get_2gis_organization_reviews_info(
        review_location.url, COUNT_REVIEWS
    )

    if new_review_data is None:
        raise Exception("Ошибка при парсинге отзывов из 2gis")

    _delete_old_data()

    _create_reviews(new_review_data["reviews"], review_location)
    _create_average_review(new_review_data["average_review"])


def _get_review_location_to_parse(location_name: str) -> ReviewLocation:
    """
    Получение объекта локации по его названию и обработка исключения.
    :param location_name: Название локации отзыва;
    :return Объект локации.
    """

    try:
        return get_object_or_404(ReviewLocation, name=location_name)
    except Exception as e:
        raise Exception(
            f"В базе данных не найдена запись с переданным названием локации: {location_name}"
        ) from e


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
        )


def _create_average_review(average_review: float) -> None:
    """
    Обновление записи о средней оценке в БД.
    :param average_review: Средняя оценка.
    """

    InformationAboutCompany.objects.update_or_create(
        block="average_review", defaults={"content": average_review}
    )


update_review()
