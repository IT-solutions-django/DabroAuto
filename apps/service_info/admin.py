from django.contrib import admin

from apps.service_info.models import (
    SocialMedia,
    StagesOfWork,
    ContactInformation,
    InformationAboutCompany,
    Settings,
    Questionnaire,
)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    """Класс админ-панели социальной сети автосалона"""

    search_fields = ("name",)


@admin.register(StagesOfWork)
class StagesOfWorkAdmin(admin.ModelAdmin):
    """Класс админ-панели этапов работы автосалона"""

    search_fields = ("name", "position")
    ordering = ("position",)


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    """Класс админ-панели контактной информации автосалона"""

    search_fields = ("name",)


@admin.register(InformationAboutCompany)
class InformationAboutCompanyAdmin(admin.ModelAdmin):
    """Класс админ-панели с информацией об автосалоне"""

    search_fields = ("block",)
    fields = ("block", "content")


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    """Класс админ-панели с информацией об обратной связи"""

    search_fields = ("name",)
    fields = ("name", "phone_number", "content", "created_at")
    readonly_fields = ("created_at",)
