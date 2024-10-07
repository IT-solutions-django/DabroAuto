from django import forms
from django.shortcuts import get_object_or_404

from apps.catalog.models import CarMark, CarModel, Country, CarPriv, CarColor


class CarSearchForm(forms.Form):
    mark = forms.ChoiceField(required=False)
    year_from = forms.ChoiceField(
        choices=[(None, "Год от")] + [(str(i), str(i)) for i in range(1980, 2025)],
        required=False,
    )
    year_to = forms.ChoiceField(
        choices=[(None, "до")] + [(str(i), str(i)) for i in range(1980, 2025)],
        required=False,
    )
    eng_v_from = forms.ChoiceField(
        choices=[(None, "Объем от")]
        + [
            ("800", "0.8L"),
            ("1000", "1.0L"),
            ("1200", "1.2L"),
            ("1500", "1.5L"),
            ("1600", "1.6L"),
            ("2000", "2.0L"),
            ("2500", "2.5L"),
            ("3000", "3.0L"),
            ("4000", "4.0L"),
            ("5000", "5.0L"),
        ],
        required=False,
    )
    eng_v_to = forms.ChoiceField(
        choices=[(None, "до")]
        + [
            ("800", "0.8L"),
            ("1000", "1.0L"),
            ("1200", "1.2L"),
            ("1500", "1.5L"),
            ("1600", "1.6L"),
            ("2000", "2.0L"),
            ("2500", "2.5L"),
            ("3000", "3.0L"),
            ("4000", "4.0L"),
            ("5000", "5.0L"),
        ],
        required=False,
    )
    kpp_type = forms.ChoiceField(
        choices=[(None, "Тип КПП")]
        + [
            ("1", "Механика"),
            ("2", "Автомат"),
        ],
        required=False,
    )
    model = forms.ChoiceField(required=False)
    mileage_from = forms.ChoiceField(
        choices=[(None, "Пробег от")]
        + [
            ("10000", "10,000 км"),
            ("20000", "20,000 км"),
            ("30000", "30,000 км"),
            ("40000", "40,000 км"),
            ("50000", "50,000 км"),
            ("60000", "60,000 км"),
            ("70000", "70,000 км"),
            ("80000", "80,000 км"),
            ("90000", "90,000 км"),
            ("100000", "100,000 км"),
            ("120000", "120,000 км"),
            ("150000", "150,000 км"),
            ("180000", "180,000 км"),
            ("200000", "200,000 км"),
        ],
        required=False,
    )
    mileage_to = forms.ChoiceField(
        choices=[(None, "до")]
        + [
            ("10000", "10,000 км"),
            ("20000", "20,000 км"),
            ("30000", "30,000 км"),
            ("40000", "40,000 км"),
            ("50000", "50,000 км"),
            ("60000", "60,000 км"),
            ("70000", "70,000 км"),
            ("80000", "80,000 км"),
            ("90000", "90,000 км"),
            ("100000", "100,000 км"),
            ("120000", "120,000 км"),
            ("150000", "150,000 км"),
            ("180000", "180,000 км"),
            ("200000", "200,000 км"),
        ],
        required=False,
    )
    priv = forms.ChoiceField(required=False)
    color = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        country_table_name = kwargs.pop("country", None)
        super().__init__(*args, **kwargs)

        country = get_object_or_404(Country, table_name=country_table_name)

        self.fields["mark"].choices = [(None, "Марка авто")] + [
            (mark.id, mark.name)
            for mark in CarMark.objects.filter(country_manufacturing=country)
        ]
        self.fields["model"].choices = [(None, "Модель авто")] + [
            (model.id, model.name) for model in CarModel.objects.all()
        ]
        self.fields["priv"].choices = [(None, "Привод")] + [
            (priv.id, priv.name)
            for priv in CarPriv.objects.filter(country_manufacturing=country)
        ]
        self.fields["color"].choices = [(None, "Цвет")] + [
            (color.id, color.name)
            for color in CarColor.objects.filter(country_manufacturing=country)
        ]
