from dataclasses import asdict
from typing import Any

from django.http import JsonResponse
from django.views import View
from django.views.generic import FormView

from apps.catalog.models import CarModel
from apps.service_info.models import ContactInformation, SocialMedia
from business.catalog_parser import get_cars_info, get_popular_cars
from pages.catalog_page.forms import CarSearchForm
from pages.home.forms import QuestionnaireForm
from utils.get_user_ip import get_user_ip
from utils.pagination import get_page_range

CARS_PER_PAGE = 12
COUNT_POPULAR_CARS = 5


class CatalogView(FormView):
    """View для отображения каталога автомобилей"""

    form_class = CarSearchForm
    template_name = "catalog_page/index.html"
    success_url = "/"
    cars_per_page = CARS_PER_PAGE
    count_popular_cars = COUNT_POPULAR_CARS
    country = None
    name = None
    table_name = None
    logo = None

    def form_valid(self, form, *args, **kwargs):
        """
        Если форма валидна, вернем код 200
        """
        user_ip = get_user_ip(self.request)

        cars_info, pages_count = get_cars_info(
            self.table_name,
            form.data,
            "1",
            self.cars_per_page,
            user_ip,
        )
        cars = [asdict(car) for car in cars_info]
        page_range = get_page_range(1, pages_count)
        return JsonResponse({"cars_info": cars, "page_range": page_range}, status=200)

    def form_invalid(self, form):
        """
        Если форма невалидна, возвращаем код 400 с ошибками.
        """
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)
        context["name"] = self.name

        if self.name == 'Японии':
            context["title"] = "Автомобиль из Японии с аукциона: каталог 2024 с ценами и фото - DAbroAUTO"
            context['description'] = ("Авто из Японии с аукциона под заказ. ⚡ Русификация и "
                                      "доставка в любые регионы РФ! ⭐ Растаможка, договор и "
                                      "полная пошлина. Помощь с выбором и поиском.")
        elif self.name == 'Кореи':
            context['title'] = "Купить авто из Кореи под заказ: каталог 2024 с ценами и фото - DAbroAUTO"
            context['description'] = ("Продажа автомобилей с аукционов Южной Кореи с русификацией. "
                                      "Доставка в любые регионы РФ. ⭐ Растаможка, договор и "
                                      "полная пошлина. ⚡Помощь с выбором и поиском.")
        elif self.name == 'Китая':
            context['title'] = "Авто из Китая под ключ с русификацией: каталог 2024 - DAbroAUTO"
            context['description'] = ("Дилеры китайских автомобилей во Владивостоке: под заказ с "
                                      "доставкой в любые регионы РФ. ⭐ Растаможка, "
                                      "договор и полная пошлина. ⚡ Помощь с выбором и поиском.")

        user_ip = get_user_ip(self.request)

        cars_info, pages_count = get_cars_info(
            self.table_name,
            self.request.GET,
            self.request.GET.get("page", "1"),
            self.cars_per_page,
            user_ip,
        )

        context["popular_cars"] = get_popular_cars(
            self.country, self.count_popular_cars
        )

        context["cars_info"] = cars_info
        context["pages_count"] = pages_count

        current_page = int(self.request.GET.get("page", 1))
        context["current_page"] = current_page

        # Определяем диапазон страниц для отображения
        context["page_range"] = get_page_range(current_page, pages_count)

        context["questionnaire_form"] = QuestionnaireForm

        context["logo"] = self.logo

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

        context["ordering_params"] = [
            ("new", "Сначала новые"),
            ("old", "Сначала старые"),
            ("low_eng_v", "С низким объемом"),
            ("high_eng_v", "С высоким объемом"),
        ]

        if self.table_name == "stats":
            context["ordering_params"].extend(
                [
                    ("new_auc_date", "С наиболее свежей датой аукциона"),
                    ("old_auc_date", "С наиболее давней датой аукциона"),
                ]
            )

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["country"] = self.table_name
        kwargs["initial"] = self.request.GET

        return kwargs


class CarModelListView(View):
    def get(self, request, *args, **kwargs):
        mark_id = request.GET.get("mark_id")
        models = CarModel.objects.filter(mark_id=mark_id).values("id", "name") or []
        return JsonResponse(list(models), safe=False)
