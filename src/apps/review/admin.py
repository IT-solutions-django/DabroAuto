from django.contrib import admin

from src.apps.review.models import ReviewLocation, ReviewAuthor, Review


@admin.register(ReviewLocation)
class ReviewLocationAdmin(admin.ModelAdmin):
    """Класс админ-панели площадки на которой расположен отзыв оставленный автосалону"""

    search_fields = ("name",)
    pass


@admin.register(ReviewAuthor)
class ReviewAuthorAdmin(admin.ModelAdmin):
    """Класс админ-панели автора отзыва оставленного автосалону"""

    search_fields = ("first_name", "last_name")
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс админ-панели отзыва оставленного автосалону"""

    autocomplete_fields = ("location", "author")
    search_fields = ("author__first_name", "author__last_name", "stars")
