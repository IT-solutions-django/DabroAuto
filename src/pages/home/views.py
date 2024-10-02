from typing import Any

from django.views.generic import TemplateView

from src.apps.car.models import Car
from src.apps.clip.models import Clip
from src.apps.review.models import Review, ReviewLocation
from src.apps.service_info.models import (
    SocialMedia,
    ContactInformation,
    InformationAboutCompany,
    StagesOfWork,
)


class HomeView(TemplateView):
    """View для отображения главной страницы"""

    template_name = "home/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)
        context["title"] = "Главная"

        context["korea_cars"] = Car.objects.filter(country_manufacturing__name="Корея")
        context["china_cars"] = Car.objects.filter(country_manufacturing__name="Китай")
        context["japan_cars"] = Car.objects.filter(country_manufacturing__name="Япония")

        context["clips"] = Clip.objects.all()

        context["phone_number_main"] = ContactInformation.objects.get(
            name="Основной номер телефона",
        ).content
        context["years_on_market"] = InformationAboutCompany.objects.get(
            block="Лет на рынке",
        ).content
        context["count_satisfied_customers"] = InformationAboutCompany.objects.get(
            block="Довольных клиентов",
        ).content
        context["average_review"] = InformationAboutCompany.objects.get(
            block="Средний рейтинг",
        ).content
        context["about_us"] = InformationAboutCompany.objects.get(
            block="О нас",
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

        context["review_locations"] = ReviewLocation.objects.all()
        context["stages_of_work"] = list(StagesOfWork.objects.all())
        context["reviews"] = Review.objects.all().select_related("author", "location")
        context["review_locations"] = ReviewLocation.objects.all()

        return context
