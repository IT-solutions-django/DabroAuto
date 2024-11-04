from django.urls import path
from django.views.decorators.cache import cache_page

from config.settings import CACHE_TIMEOUT
from pages.car_card.views import CarCardView
from pages.catalog_page.views import (
    CarModelListView,
    CatalogView,
)
from pages.home.views import HomeView, home

urlpatterns = [
    path(
        "japan/<str:id>/",
        cache_page(CACHE_TIMEOUT)(
            CarCardView.as_view(country="Япония", title="Японии")
        ),
        name="car-card-japan",
    ),
    path(
        "korea/<str:id>/",
        cache_page(CACHE_TIMEOUT)(CarCardView.as_view(country="Корея", title="Кореи")),
        name="car-card=korea",
    ),
    path(
        "china/<str:id>/",
        cache_page(CACHE_TIMEOUT)(CarCardView.as_view(country="Китай", title="Китая")),
        name="car-card-china",
    ),
    path(
        "japan/",
        cache_page(CACHE_TIMEOUT)(
            CatalogView.as_view(
                country="Япония", name="Японии", table_name="stats", logo="flag2.png"
            )
        ),
        name="japan-page",
    ),
    path(
        "korea/",
        cache_page(CACHE_TIMEOUT)(
            CatalogView.as_view(
                country="Корея", name="Кореи", table_name="main", logo="flag.svg"
            )
        ),
        name="korea-page",
    ),
    path(
        "china/",
        cache_page(CACHE_TIMEOUT)(
            CatalogView.as_view(
                country="Китай", name="Китая", table_name="china", logo="flag3.svg"
            )
        ),
        name="china-page",
    ),
    path(
        "models/", cache_page(CACHE_TIMEOUT)(CarModelListView.as_view()), name="models"
    ),
    path("", home, name="home"),
]
