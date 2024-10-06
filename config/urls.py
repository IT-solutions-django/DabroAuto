from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from pages.admin_settings_integration.views import SettingsIntegrationView
from pages.home.views import HomeView

urlpatterns = [
    path(
        "admin/settings-integration/update-playlists/",
        SettingsIntegrationView.as_view(),
        name="update_playlists",
    ),
    path(
        "admin/settings-integration/",
        SettingsIntegrationView.as_view(),
        name="settings_integration",
    ),
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
