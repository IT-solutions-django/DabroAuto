from django.urls import path

from pages.admin_settings_integration.views import SettingsIntegrationView
from pages.car_card.views import CarCardView
from pages.catalog_page.views import (
    CatalogJapanView,
    CarModelListView,
    CatalogKoreaView,
    CatalogChinaView,
)
from pages.home.views import HomeView

urlpatterns = [
    path(
        "admin/settings-integration/",
        SettingsIntegrationView.as_view(),
        name="settings_integration",
    ),
    path("catalog-japan/<str:id>/", CarCardView.as_view(), name="car-card"),
    path("catalog-japan/", CatalogJapanView.as_view(), name="catalog-japan-page"),
    path("catalog-korea/", CatalogKoreaView.as_view(), name="catalog-korea-page"),
    path("catalog-china/", CatalogChinaView.as_view(), name="catalog-china-page"),
    path("models/", CarModelListView.as_view(), name="models"),
    path("", HomeView.as_view(), name="home"),
]
