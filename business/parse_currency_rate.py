import requests

from apps.catalog.models import CurrencyRate


def update_currency_rate():
    res = requests.get("https://auc.tda04.ru/currency")
    data = res.json()

    CurrencyRate.objects.update_or_create(
        name="Евро",
        defaults={"course": data["eur"]},
    )
    CurrencyRate.objects.update_or_create(
        name="Доллар",
        defaults={"course": data["usd"]},
    )
