from django.urls import path

from pages.car_card.views import CarCardView
from pages.catalog_page.views import (
    CarModelListView,
    CatalogView,
)
from pages.home.views import HomeView

urlpatterns = [
    path(
        "japan/<str:id>/",
        CarCardView.as_view(country="Япония", title="Японии"),
        name="car-card-japan",
    ),
    path(
        "korea/<str:id>/",
        CarCardView.as_view(country="Корея", title="Кореи"),
        name="car-card=korea",
    ),
    path(
        "china/<str:id>/",
        CarCardView.as_view(country="Китай", title="Китая"),
        name="car-card-china",
    ),
    path(
        "japan/",
        CatalogView.as_view(
            country="Япония", name="Японии", table_name="stats", logo="flag2.png"
        ),
        name="japan-page",
    ),
    path(
        "korea/",
        CatalogView.as_view(
            country="Корея", name="Кореи", table_name="main", logo="flag.svg"
        ),
        name="korea-page",
    ),
    path(
        "china/",
        CatalogView.as_view(
            country="Китай", name="Китая", table_name="china", logo="flag3.svg"
        ),
        name="china-page",
    ),
    path("models/", CarModelListView.as_view(), name="models"),
    path("", HomeView.as_view(), name="home"),
]
