from django.contrib import admin

from src.apps.clip.models import Clip


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    search_fields = ("name", "url")
