from typing import Any

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import FormView

from apps.catalog.models import CarMark, CarModel
from pages.catalog_page.forms import CarSearchForm


class CatalogView(FormView):
    """View для отображения главной страницы"""

    form_class = CarSearchForm
    template_name = "catalog_page/index.html"
    success_url = "/"

    def form_valid(self, form, *args, **kwargs):
        """
        Если форма валидна, вернем код 200
        """
        print(form.data)
        return JsonResponse({}, status=200)

    def form_invalid(self, form):
        """
        Если форма невалидна, возвращаем код 400 с ошибками.
        """
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)
        context["title"] = "Каталог"

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        country = "stats"
        kwargs["country"] = country
        return kwargs


class CarModelListView(View):
    def get(self, request, *args, **kwargs):
        mark_id = request.GET.get("mark_id")
        models = CarModel.objects.filter(mark_id=mark_id).values("id", "name") or []
        return JsonResponse(list(models), safe=False)
