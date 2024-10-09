from typing import Any

from django.views.generic import FormView, TemplateView

from business.catalog_parser import get_car_by_id


class CarCardView(TemplateView):
    """View для отображения каталога Китайских автомобилей"""

    template_name = "car_card/index.html"
    country = "Япония"

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        car_id = kwargs["id"]
        context["title"] = "Карточка Автомобиля"
        context["name"] = self.country

        context["car"] = get_car_by_id(self.country, car_id)
        print(context["car"])

        return context
