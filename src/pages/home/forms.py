from django import forms

from src.apps.service_info.models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    privacy_policy_agreed = forms.BooleanField(
        required=True,
        error_messages={"required": "Вы должны согласиться с политикой безопасности."},
    )

    class Meta:
        model = Questionnaire
        fields = ["name", "phone_number", "content", "privacy_policy_agreed"]
