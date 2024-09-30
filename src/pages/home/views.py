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
        context["cars"] = Car.objects.all().select_related(
            "brand", "model", "engine_type", "country_manufacturing"
        )
        context["reviews"] = Review.objects.all().select_related("author", "location")
        context["review_locations"] = ReviewLocation.objects.all()
        context["social_media"] = SocialMedia.objects.all()
        context["contact_information"] = ContactInformation.objects.all()
        context["stages_of_work"] = StagesOfWork.objects.all()
        context["information_about_company"] = InformationAboutCompany.objects.all()
        context["clips"] = Clip.objects.all()
        return context


9
