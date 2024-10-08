from django.urls import path

from pages.admin_settings_integration.views import SettingsIntegrationView
from pages.catalog_page.views import CatalogView, CarModelListView
from pages.home.views import HomeView

urlpatterns = [
    path(
        "admin/settings-integration/",
        SettingsIntegrationView.as_view(),
        name="settings_integration",
    ),
    path("catalog/", CatalogView.as_view(), name="catalog-page"),
    path("models/", CarModelListView.as_view(), name="models"),
    path("", HomeView.as_view(), name="home"),
]
