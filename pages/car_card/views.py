from dataclasses import asdict
from typing import Any

from django.views.generic import FormView, TemplateView
from apps.catalog.models import CurrencyRate
from apps.service_info.models import SocialMedia, ContactInformation
from business.catalog_parser import get_car_by_id, get_cars_info
from pages.home.forms import QuestionnaireForm
from utils.get_user_ip import get_user_ip

from apps.catalog.models import Country, CarMark


class CarCardView(TemplateView):
    """View для отображения каталога Китайских автомобилей"""

    template_name = "car_card/index.html"
    country = None
    title = None

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        car_id = kwargs["id"]

        url_name = self.request.resolver_match.url_name
        context['url_name'] = url_name

        user_ip = get_user_ip(self.request)

        context["title"] = "Карточка Автомобиля"
        context["name"] = self.title

        car, main_page_car = get_car_by_id(self.country, car_id, user_ip)
        context["car"] = car
        context['main_page_car'] = main_page_car
        context["country"] = self.country

        context["eur"] = float(CurrencyRate.objects.get(name="Евро").course)
        context["dollar"] = float(CurrencyRate.objects.get(name="Доллар").course)

        if self.country == 'Япония':
            context['url_catalog_cars'] = 'japan'
        elif self.country == 'Китай':
            context['url_catalog_cars'] = 'china'
        else:
            context['url_catalog_cars'] = 'korea'

        try:
            id_car = CarMark.objects.get(name=car.mark, country_manufacturing__name=self.country).id
        except Exception:
            id_car = None

        country = Country.objects.get(name=self.country)
        table_name = country.table_name

        if id_car:
            cars_info_recommend, pages_count = get_cars_info(
                table_name,
                {'mark': id_car, 'year_from': 2020, 'year_to': 2021,
                 'ordering': 'high_eng_v'},
                "1",
                5,
                user_ip,
            )

            cars_recommend = [asdict(car) for car in cars_info_recommend]

            context['cars_recommend'] = cars_recommend

        context["questionnaire_form"] = QuestionnaireForm

        context["phone_number_main"] = ContactInformation.objects.get_or_create(
            name="Основной номер телефона", defaults={"content": "8 (800) 500-49-46"}
        )[0].content

        context["tg_url"] = SocialMedia.objects.get_or_create(
            name="Телеграм-канал", defaults={"url": "https://t.me/batareyka25rus"}
        )[0].url
        context["vk_url"] = SocialMedia.objects.get_or_create(
            name="VK",
            defaults={
                "url": "https://vk.com/batareyka25rus?ysclid=m2cvbntabv851406401"
            },
        )[0].url
        context["inst_url"] = SocialMedia.objects.get_or_create(
            name="Instagram", defaults={"url": "https://t.me/batareyka25rus"}
        )[0].url

        context["phone_number"] = ContactInformation.objects.get_or_create(
            name="Номер телефона", defaults={"content": "8 800 550 48 32"}
        )[0].content
        context["whatsapp"] = ContactInformation.objects.get_or_create(
            name="WhatsApp", defaults={"content": "+7 (924) 420-24-32"}
        )[0].content
        context["address"] = ContactInformation.objects.get_or_create(
            name="Адрес", defaults={"content": "г. Владивосток, ул. Тополевая 6"}
        )[0].content
        context["whatsapp_url"] = (
            f"https://wa.me/{''.join(i for i in context["whatsapp"] if i.isdigit())}"
        )

        return context
