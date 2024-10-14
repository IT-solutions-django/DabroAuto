from typing import Any

from django.views.generic import FormView, TemplateView

from apps.service_info.models import SocialMedia, ContactInformation
from business.catalog_parser import get_car_by_id
from pages.home.forms import QuestionnaireForm


class CarCardView(TemplateView):
    """View для отображения каталога Китайских автомобилей"""

    template_name = "car_card/index.html"
    country = None

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        car_id = kwargs["id"]

        context["title"] = "Карточка Автомобиля"
        context["name"] = self.country

        context["car"] = get_car_by_id(self.country, car_id)
        context["country"] = self.country

        context["questionnaire_form"] = QuestionnaireForm

        context["phone_number_main"] = ContactInformation.objects.get(
            name="Основной номер телефона",
        ).content

        context["tg_url"] = SocialMedia.objects.get(name="Телеграм-канал").url
        context["vk_url"] = SocialMedia.objects.get(name="VK").url
        context["inst_url"] = SocialMedia.objects.get(name="Instagram").url

        context["phone_number"] = ContactInformation.objects.get(
            name="Номер телефона",
        ).content
        context["whatsapp"] = ContactInformation.objects.get(
            name="WhatsApp",
        ).content
        context["whatsapp_url"] = (
            f"https://wa.me/{''.join(i for i in context["whatsapp"] if i.isdigit())}"
        )
        context["address"] = ContactInformation.objects.get(
            name="Адрес",
        ).content

        return context
