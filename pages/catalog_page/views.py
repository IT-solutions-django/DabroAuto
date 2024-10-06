from typing import Any

from django.http import JsonResponse
from django.views.generic import FormView

from pages.catalog_page.forms import CarSearchForm


class CatalogView(FormView):
    """View для отображения главной страницы"""

    form_class = CarSearchForm
    template_name = "catalog_page/index.html"
    success_url = "/"

    def form_valid(self, form):
        """
        Если форма валидна, вернем код 200
        """
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
