from django.contrib import admin

from apps.clip.models import Clip, ClipPlatform


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    search_fields = ("name", "url")


@admin.register(ClipPlatform)
class ClipPlatformAdmin(admin.ModelAdmin):
    search_fields = ("name", "url")
