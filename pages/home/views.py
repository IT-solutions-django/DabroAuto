from typing import Any
from django.shortcuts import render, redirect
from collections import defaultdict

from django.http import JsonResponse
from django.views.generic import FormView
from django.conf import settings
from apps.car.models import Car
from apps.catalog.models import CarMark
from apps.clip.models import Clip
from apps.review.models import Review, ReviewLocation
from apps.service_info.models import (
    SocialMedia,
    ContactInformation,
    InformationAboutCompany,
    StagesOfWork,
)
from pages.home.forms import QuestionnaireForm, DeliveryForm
from tasks.tasks import telegram_send_mail_for_all_task, email_send_task
from apps.delivery.models import Delivery


class HomeView(FormView):
    """View для отображения главной страницы"""

    form_class = QuestionnaireForm
    template_name = "home/index.html"
    success_url = "/"

    def form_valid(self, form):
        """
        Если форма валидна, вернем код 200
        """
        message = form.save()
        telegram_send_mail_for_all_task.delay(
            "Обратная связь с сайта DabroAuto\n\n"
            f"Автор: {message.name}\n\n"
            f"Номер телефона: {message.phone_number}\n\n"
            f"Содержание: {message.content}",
        )
        return JsonResponse({}, status=200)

    def form_invalid(self, form):
        """
        Если форма невалидна, возвращаем код 400 с ошибками.
        """
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        delivery = Delivery.objects.select_related('city').order_by('city__name')
        unique_body_types = get_distinct()

        context = super().get_context_data(id=id, **kwargs)
        context["title"] = "Авто с аукционов Японии, Китая и Кореи с русификацией - DAbroAUTO"
        context['description'] = ("Привезем авто с аукционов Японии, Китая и Кореи под ключ с "
                                  "растаможкой и доставкой в регионы. ⭐ Каталог с ценами и фото! ⚡ "
                                  "Рассчитать стоимость доставки можно на нашем сайте.")

        context['delivery'] = delivery
        context['unique_body_types'] = unique_body_types

        context["korea_cars"] = Car.objects.filter(country_manufacturing__name="Корея")
        context["china_cars"] = Car.objects.filter(country_manufacturing__name="Китай")
        context["japan_cars"] = Car.objects.filter(country_manufacturing__name="Япония")

        context["clips"] = Clip.objects.all()

        context["phone_number_main"] = ContactInformation.objects.get_or_create(
            name="Основной номер телефона", defaults={"content": "8 (800) 500-49-46"}
        )[0].content
        context["years_on_market"] = InformationAboutCompany.objects.get_or_create(
            block="Лет на рынке", defaults={"content": "5"}
        )[0].content
        context["count_satisfied_customers"] = (
            InformationAboutCompany.objects.get_or_create(
                block="Довольных клиентов", defaults={"content": "4 000"}
            )[0].content
        )
        context["average_review"] = InformationAboutCompany.objects.get_or_create(
            block="Средний рейтинг", defaults={"content": "5.0"}
        )[0].content
        context["about_us"] = InformationAboutCompany.objects.get_or_create(
            block="О нас", defaults={"content": "текст о нас"}
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

        context["review_locations"] = ReviewLocation.objects.all()
        context["stages_of_work"] = list(StagesOfWork.objects.all())
        context["reviews"] = Review.objects.all().select_related("author", "location")
        context["review_locations"] = ReviewLocation.objects.all()

        context["brands_ids_to_logos"] = [
            ("japan", get_car_brand_id_or_none("BMW", "Япония")),
            ("japan", get_car_brand_id_or_none("TOYOTA", "Япония")),
            ("japan", get_car_brand_id_or_none("AUDI", "Япония")),
            ("china", get_car_brand_id_or_none("KIA", "Китай")),
            ("japan", get_car_brand_id_or_none("MERCEDES BENZ", "Япония")),
            ("japan", get_car_brand_id_or_none("HYUNDAI", "Япония")),
            ("china", get_car_brand_id_or_none("CHERY", "Китай")),
            ("china", get_car_brand_id_or_none("CHEVROLET", "Китай")),
            ("japan", get_car_brand_id_or_none("RENAULT", "Япония")),
            ("china", get_car_brand_id_or_none("HAVAL", "Китай")),
            ("china", get_car_brand_id_or_none("JAC", "Китай")),
            ("korea", get_car_brand_id_or_none("DAEVOO", "Корея")),
            ("china", get_car_brand_id_or_none("FAW", "Китай")),
        ]

        return context


def get_car_brand_id_or_none(name: str, country_manufacturing: str):
    try:
        return CarMark.objects.get(
            name=name, country_manufacturing__name=country_manufacturing
        ).id
    except Exception:
        return None


def get_distinct():
    deliveries = Delivery.objects.select_related('body_type').values('city', 'body_type__name', 'price')
    city_body_map = defaultdict(lambda: defaultdict(list))

    for delivery in deliveries:
        city_body_map[delivery['city']][delivery['body_type__name']].append(delivery['price'])

    unique_body_types = set()
    for body_types in city_body_map.values():
        unique_body_types.update(body_types.keys())

    unique_body_types = list(unique_body_types)

    return unique_body_types


def home(request):
    korea_cars = Car.objects.filter(country_manufacturing__name="Корея")[:4]
    china_cars = Car.objects.filter(country_manufacturing__name="Китай")[:4]
    japan_cars = Car.objects.filter(country_manufacturing__name="Япония")[:4]

    reviews = Review.objects.all()

    car_type_choices = [
        ('sedan', 'Седан'),
        ('crossover', 'Кроссовер'),
        ('suv', 'Внедорожник')
    ]

    form_1 = DeliveryForm()
    form_1.fields['car_type'].choices = car_type_choices

    form_2 = QuestionnaireForm()

    return render(
        request, 'home/index.html',
        {
            'form': form_1,
            'japan_cars': japan_cars,
            'korea_cars': korea_cars,
            'china_cars': china_cars,
            'form_2': form_2,
            'reviews': reviews
        }
    )


def post_questionnaire_form(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        message = form.save()
        telegram_send_mail_for_all_task.delay(
            "Обратная связь с сайта DabroAuto\n\n"
            f"Автор: {message.name}\n\n"
            f"Номер телефона: {message.phone_number}\n\n"
            f"Содержание: {message.content}",
        )
        email_send_task.delay(
            subject="Обратная связь с сайта DabroAuto",
            message=(
                f"Автор: {message.name}\n\n"
                f"Номер телефона: {message.phone_number}\n\n"
                f"Содержание: {message.content}"
            ),
            recipient_list=[settings.CONTACT_EMAIL]
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))
