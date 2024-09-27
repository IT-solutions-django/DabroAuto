from django.shortcuts import get_object_or_404

from src.apps.review.models import Review, ReviewAuthor, ReviewLocation
from src.apps.service_info.models import InformationAboutCompany
from src.business.parsing_review import ReviewParser, ReviewParser2GIS

REVIEWS_LOCATION_NAME = "2gis"
COUNT_REVIEWS = 20


def update_review():
    Review.objects.all().delete()
    ReviewAuthor.objects.all().delete()

    review_location = get_object_or_404(ReviewLocation, name="2gis")

    parser = ReviewParser(
        ReviewParser2GIS,
        review_location.url,
    )
    parser.load_html()
    reviews = parser.parse_review()[:COUNT_REVIEWS]

    for review in reviews:
        review_author = ReviewAuthor.objects.create(
            first_name=review["first_name"], last_name=review["last_name"]
        )
        Review.objects.create(
            stars=review["stars"], author=review_author, location=review_location
        )

    average_review = parser.parce_average_review()
    InformationAboutCompany.objects.update_or_create(
        block="average_review", defaults={"content": average_review}
    )


update_review()
