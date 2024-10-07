import json
from typing import Any

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView

from business.settings_integration_client import (
    get_settings_integration_config,
    save_to_json,
)
from pages.admin_settings_integration.forms import IntegrationConfigForm


class SettingsIntegrationView(FormView):
    json_file_path = "config/settings_integration.json"
    form_class = IntegrationConfigForm
    template_name = "admin_settings_integration/index.html"
    success_url = "/admin/settings-integration/"

    def form_valid(self, form, *args, **kwargs):
        """
        Если форма валидна, вернем код 200
        """
        new_data = {
            "youtube_channel_url": form.data["youtube_channel_url"],
            "youtube_count_videos": form.data["youtube_count_videos"],
            "youtube_playlists": form.data["youtube_playlists"].split(", "),
            "reviews_service_name": form.data["reviews_service_name"],
            "reviews_count": form.data["reviews_count"],
        }
        save_to_json(new_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Если форма невалидна, возвращаем код 400 с ошибками.
        """
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Настройки интеграции"

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        settings_integration_config = get_settings_integration_config()

        kwargs["initial"] = settings_integration_config
        kwargs["initial"]["youtube_playlists"] = ", ".join(
            settings_integration_config["youtube_playlists"]
        )

        return kwargs
