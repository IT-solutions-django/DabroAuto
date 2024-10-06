import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from pages.admin_settings_integration.forms import IntegrationConfigForm


class SettingsIntegrationView(View):
    json_file_path = "config/settings_integration.json"

    def get(self, request):
        # Чтение данных из JSON-файла
        with open(self.json_file_path, "r") as json_file:
            data = json.load(json_file)

        form = IntegrationConfigForm(initial=data)
        return render(request, "admin_settings_integration/index.html", {"form": form})

    def post(self, request):
        form = IntegrationConfigForm(request.POST)
        if form.is_valid():
            # Сохранение данных в JSON-файл
            new_data = {
                "youtube_channel_url": form.cleaned_data["youtube_channel_url"],
                "youtube_count_videos": form.cleaned_data["youtube_count_videos"],
                "youtube_playlists": form.cleaned_data["youtube_playlists"],
                "reviews_service_name": form.cleaned_data["reviews_service_name"],
                "reviews_count": form.cleaned_data["reviews_count"],
            }
            with open(self.json_file_path, "w") as json_file:
                json.dump(new_data, json_file, indent=4)
            return redirect("settings_integration")  # Перенаправление после сохранения

        return render(request, "admin_settings_integration/index.html", {"form": form})

    def update_playlists(self, request):
        print(1111)
        if request.method == "POST":
            channel_url = request.POST.get("youtube_channel_url")
            form = IntegrationConfigForm(initial={"youtube_channel_url": channel_url})
            form.fields["youtube_playlists"].choices = form.get_playlists(channel_url)
            playlists = form.fields["youtube_playlists"].choices
            return JsonResponse(
                {"playlists": [{"id": id, "title": title} for id, title in playlists]}
            )
