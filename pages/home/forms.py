from django import forms

from apps.service_info.models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    privacy_policy_agreed = forms.BooleanField(
        required=True,
        error_messages={"required": "Вы должны согласиться с политикой безопасности."},
        initial=True,
    )

    class Meta:
        model = Questionnaire
        fields = ["name", "phone_number", "content", "privacy_policy_agreed"]
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
                    "pattern": r"^\+7 \d{3} \d{3} \d{2} \d{2}$",
                    "title": "Формат: '+7 999 999 99 99'",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Введите текст сообщения, укажите страну, марку и год машины.",
                    "maxlength": "200",
                }
            ),
            "privacy_policy_agreed": forms.CheckboxInput(),
        }
