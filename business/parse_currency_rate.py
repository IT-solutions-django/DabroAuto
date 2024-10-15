import requests
from bs4 import BeautifulSoup

from apps.catalog.models import CurrencyRate


def update_currency_rate():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0"
    }
    res = requests.get("https://pskb.com/currency/", headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    rows = soup.find_all("tr")
    currency_rates = {}

    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            currency_code = cells[0].strong.text  # Код валюты
            if currency_code == "USD" or currency_code == "EUR":
                # Курс ЦБ из последней колонки
                currency_rates[currency_code] = float(cells[3].text)
            elif currency_code in ["CNY", "JPY", "KRW"]:
                # Курс продажи из предпоследней колонки
                currency_rates[currency_code] = float(cells[2].text)

    CurrencyRate.objects.update_or_create(
        name="Евро",
        defaults={"course": currency_rates["EUR"]},
    )
    CurrencyRate.objects.update_or_create(
        name="Доллар",
        defaults={"course": currency_rates["USD"]},
    )
    CurrencyRate.objects.update_or_create(
        name="Юань",
        defaults={"course": currency_rates["CNY"] / 10},
    )
    CurrencyRate.objects.update_or_create(
        name="Иена",
        defaults={"course": currency_rates["JPY"] / 100},
    )
    CurrencyRate.objects.update_or_create(
        name="Вона",
        defaults={"course": currency_rates["KRW"] / 1000},
    )
