from django.contrib import admin

from src.apps.service_info.models import (
    SocialMedia,
    StagesOfWork,
    ContactInformation,
    InformationAboutCompany,
)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    """Класс админ-панели социальной сети автосалона"""

    search_fields = ("name",)


@admin.register(StagesOfWork)
class StagesOfWorkAdmin(admin.ModelAdmin):
    """Класс админ-панели этапов работы автосалона"""

    search_fields = ("name",)


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    """Класс админ-панели контактной информации автосалона"""

    search_fields = ("name",)


@admin.register(InformationAboutCompany)
class InformationAboutCompanyAdmin(admin.ModelAdmin):
    """Класс админ-панели с информацией об автосалоне"""

    search_fields = ("block",)
    fields = ("block", "content")
