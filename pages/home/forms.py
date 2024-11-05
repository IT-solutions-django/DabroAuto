from django import forms

from apps.service_info.models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ["name", "phone_number", "content"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Введите имя",
                    "pattern": r"^[A-Za-zА-Яа-яЁё\s]+$",
                    "title": "Имя должно содержать только буквы и пробелы.",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "placeholder": "+7",
                    "type": "tel",
                    "pattern": r"^\+7\d{10}$",
                    "title": "Формат: '+7XXXXXXXXXX'",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Введите текст сообщения, укажите страну, марку и год машины.",
                    "maxlength": "200",
                }
            )
        }


class DeliveryForm(forms.Form):
    car_type = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
        label="Выберите тип авто",
        required=True
    )
    destination = forms.CharField(
        max_length=100,
        label="Пункт назначения",
        widget=forms.TextInput(attrs={
            'placeholder': 'Город назначения',
            'class': 'city-input'
        })
    )
