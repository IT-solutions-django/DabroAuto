import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from apps.catalog.models import CurrencyRate

HEADERS = {
    "Sec-Ch-Ua": '"Chromium";v="129", "Not=A?Brand";v="8"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
}


def update_currency_rate():
    headers = {
        **HEADERS,
        "User-Agent": UserAgent().random,
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
