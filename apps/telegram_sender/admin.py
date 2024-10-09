from django.contrib import admin

from apps.telegram_sender.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    search_fields = ("chat_id",)
