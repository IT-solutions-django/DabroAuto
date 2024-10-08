from dataclasses import asdict
from typing import Any

from django.http import JsonResponse
from django.views import View
from django.views.generic import FormView

from apps.catalog.models import CarModel
from business.catalog_parser import get_cars_info
from pages.catalog_page.forms import CarSearchForm
from utils.pagination import get_page_range

CARS_PER_PAGE = 10


class CatalogJapanView(FormView):
    """View для отображения каталога Японских автомобилей"""

    form_class = CarSearchForm
    template_name = "catalog_page/index.html"
    success_url = "/"
    cars_per_page = CARS_PER_PAGE

    def form_valid(self, form, *args, **kwargs):
        """
        Если форма валидна, вернем код 200
        """
        cars_info, pages_count = get_cars_info(
            "stats",
            form.data,
            "1",
            self.cars_per_page,
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
        context["title"] = "Каталог"
        context["name"] = "Япония"

        cars_info, pages_count = get_cars_info(
            "stats",
            self.request.GET,
            self.request.GET.get("page", "1"),
            self.cars_per_page,
        )
        context["cars_info"] = cars_info
        context["pages_count"] = pages_count

        current_page = int(self.request.GET.get("page", 1))
        context["current_page"] = current_page

        # Определяем диапазон страниц для отображения
        context["page_range"] = get_page_range(current_page, pages_count)

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["country"] = "stats"
        kwargs["initial"] = self.request.GET

        return kwargs


class CatalogChinaView(FormView):
    """View для отображения каталога Китайских автомобилей"""

    form_class = CarSearchForm
    template_name = "catalog_page/index.html"
    success_url = "/"
    cars_per_page = CARS_PER_PAGE

    def form_valid(self, form, *args, **kwargs):
        """
        Если форма валидна, вернем код 200
        """
        cars_info, pages_count = get_cars_info(
            "main",
            form.data,
            "1",
            self.cars_per_page,
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
        context["title"] = "Каталог"
        context["name"] = "Китай"

        cars_info, pages_count = get_cars_info(
            "main",
            self.request.GET,
            self.request.GET.get("page", "1"),
            self.cars_per_page,
        )
        context["cars_info"] = cars_info
        context["pages_count"] = pages_count

        current_page = int(self.request.GET.get("page", 1))
        context["current_page"] = current_page

        # Определяем диапазон страниц для отображения
        context["page_range"] = get_page_range(current_page, pages_count)

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["country"] = "main"
        kwargs["initial"] = self.request.GET

        return kwargs


class CarModelListView(View):
    def get(self, request, *args, **kwargs):
        mark_id = request.GET.get("mark_id")
        models = CarModel.objects.filter(mark_id=mark_id).values("id", "name") or []
        return JsonResponse(list(models), safe=False)
