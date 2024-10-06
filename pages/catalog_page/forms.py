from django import forms


class CarSearchForm(forms.Form):
    brand = forms.ChoiceField(
        choices=[
            ("toyota", "Toyota"),
            ("ford", "Ford"),
            ("bmw", "BMW"),
        ]
    )
    year_from = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1980, 2025)])
    year_to = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1980, 2025)])
    volume_from = forms.ChoiceField(
        choices=[
            ("1.0", "1.0L"),
            ("1.5", "1.5L"),
            ("2.0", "2.0L"),
        ]
    )
    volume_to = forms.ChoiceField(
        choices=[
            ("1.0", "1.0L"),
            ("1.5", "1.5L"),
            ("2.0", "2.0L"),
        ]
    )
    drive_type = forms.ChoiceField(
        choices=[
            ("fwd", "Передний привод"),
            ("rwd", "Задний привод"),
            ("awd", "Полный привод"),
        ]
    )
    model = forms.ChoiceField(
        choices=[
            ("model_a", "Модель A"),
            ("model_b", "Модель B"),
        ]
    )
    mileage_from = forms.ChoiceField(
        choices=[
            ("0", "0 км"),
            ("10000", "10,000 км"),
            ("20000", "20,000 км"),
        ]
    )
    mileage_to = forms.ChoiceField(
        choices=[
            ("0", "0 км"),
            ("10000", "10,000 км"),
            ("20000", "20,000 км"),
        ]
    )
    transmission_type = forms.ChoiceField(
        choices=[
            ("manual", "Механическая"),
            ("automatic", "Автоматическая"),
        ]
    )
    color = forms.ChoiceField(
        choices=[
            ("red", "Красный"),
            ("blue", "Синий"),
            ("black", "Черный"),
        ]
    )
