from typing import Iterable
from bs4 import BeautifulSoup

import requests
from django.db import transaction

from apps.catalog.models import (
    BaseFilter,
    CarMark,
    CarModel,
    CarColor,
    CarPriv,
    Country,
)
import datetime


def update_catalog_meta():
    table_name = "stats"
    base_filters = get_base_filters(table_name)
    upload_and_save_marks_and_models(table_name, base_filters.values())
    upload_and_save_colors(table_name, base_filters.values())
    upload_and_save_priv(table_name, base_filters.values())


def get_cars_info(table_name: str, filters: dict, page: str, cars_per_page: int):
    base_filters = get_base_filters(table_name)
    filters = connect_filters(filters, base_filters)
    query = get_sql_query(
        "*", table_name, filters, f"{cars_per_page * (int(page) - 1)},{cars_per_page}"
    )
    print(query)
    return fetch_by_query(query)


def connect_filters(filters: dict, base_filters: dict):
    mark_name = get_model_data_or_none(filters.get("mark"), CarMark)
    model_name = get_model_data_or_none(filters.get("model"), CarModel)
    priv = get_model_data_or_none(filters.get("priv"), CarPriv)
    color = get_model_data_or_none(filters.get("color"), CarColor)
    year_from = filters.get("year_from") or None
    year_to = filters.get("year_to") or None
    eng_v_from = filters.get("eng_v_from") or None
    eng_v_to = filters.get("eng_v_to") or None
    mileage_from = filters.get("mileage_from") or None
    mileage_to = filters.get("mileage_to") or None
    kpp_type = filters.get("kpp_type") or None

    result = [
        mark_name and f"MARKA_NAME+=+'{mark_name}'",
        model_name and f"MODEL_NAME+=+'{model_name}'",
        priv and f"PRIV+=+'{priv}'",
        color and f"COLOR+=+'{color}'",
        year_from and f"YEAR+>=+{year_from}",
        year_to and f"YEAR+<=+{year_to}",
        eng_v_from and f"ENG_V+>=+{eng_v_from}",
        eng_v_to and f"ENG_V+<=+{eng_v_to}",
        mileage_from and f"MILEAGE+>=+{mileage_from}",
        mileage_to and f"MILEAGE+<=+{mileage_to}",
        kpp_type and f"KPP_TYPE+=+'{kpp_type}'",
    ]

    if mark_name is not None:
        del base_filters["MARKA_NAME"]

    if year_to:
        del base_filters["YEAR"]

    if eng_v_from:
        del base_filters["ENG_V"]

    if mileage_to:
        del base_filters["MILEAGE"]

    if kpp_type:
        del base_filters["KPP_TYPE"]

    result.extend(base_filters.values())

    result = [res for res in result if res is not None]

    return result


def get_model_data_or_none(id: str | None, model):
    try:
        return model.objects.get(id=id).name
    except:
        return None


@transaction.atomic
def upload_and_save_priv(table_name: str, base_filters: Iterable[str]):
    CarPriv.objects.all().delete()
    country_manufacturing = Country.objects.get(table_name=table_name)
    fields = "DISTINCT+PRIV"

    for line in full_data_fetch(fields, table_name, base_filters):
        if line.get("PRIV") is None:
            continue
        CarPriv.objects.create(
            name=line["PRIV"], country_manufacturing=country_manufacturing
        )


@transaction.atomic
def upload_and_save_colors(table_name: str, base_filters: Iterable[str]):
    CarColor.objects.all().delete()
    country_manufacturing = Country.objects.get(table_name=table_name)
    fields = "DISTINCT+COLOR"

    for line in full_data_fetch(fields, table_name, base_filters):
        if line.get("COLOR") is None:
            continue
        CarColor.objects.create(
            name=line["COLOR"], country_manufacturing=country_manufacturing
        )


@transaction.atomic
def upload_and_save_marks_and_models(table_name: str, base_filters: Iterable[str]):
    CarMark.objects.all().delete()
    CarModel.objects.all().delete()
    country_manufacturing = Country.objects.get(table_name=table_name)
    fields = "DISTINCT+MODEL_NAME,+MARKA_NAME"

    for line in full_data_fetch(fields, table_name, base_filters):
        car_mark, _ = CarMark.objects.get_or_create(
            name=line["MARKA_NAME"], country_manufacturing=country_manufacturing
        )
        CarModel.objects.create(name=line["MODEL_NAME"], mark=car_mark)


def full_data_fetch(fields: str, table_name: str, base_filters: Iterable[str]):
    offset = 0
    query = get_sql_query(fields, table_name, base_filters, f"{offset},250")
    data = fetch_by_query(query)

    while len(data) > 0:
        yield from data

        offset += 250
        query = get_sql_query(fields, table_name, base_filters, f"{offset},250")
        data = fetch_by_query(query)


def fetch_by_query(sql_query: str):
    url = f"http://78.46.90.228/api/?ip=45.84.177.55&code=A25nhGfE56Kd&sql={sql_query}"
    res = requests.get(url)
    soup = BeautifulSoup(res.content.decode("utf-8"), "xml")
    return [
        {elem.name: elem.getText() for elem in row.findChildren()}
        for row in soup.findAll("row")
    ]


def get_sql_query(
    fields: str, table_name: str, base_filters: Iterable[str], limit: str
):
    query = f"select+{fields}+from+{table_name}+WHERE+1+=+1+and+{'+and+'.join(base_filters)}+limit+{limit}"
    return query


def get_base_filters(table_name: str):
    base_filers = BaseFilter.objects.get(country_manufacturing__table_name=table_name)

    max_auction_date = datetime.datetime.now() - datetime.timedelta(
        days=int(base_filers.auction_date)
    )

    kpp_types = (str(kpp_type) for kpp_type in base_filers.kpp_type)

    return {
        "AUCTION_DATE": f"AUCTION_DATE+>=+'{max_auction_date.date()}'",
        "AUCTION": f"AUCTION+NOT+LIKE+'%{base_filers.auction}%'",
        "MARKA_NAME": f"MARKA_NAME+NOT+IN+(+'{ "',+'".join(base_filers.marka_name)}'+)",
        "YEAR": f"YEAR+<=+{base_filers.year}",
        "ENG_V": f"ENG_V+>+{base_filers.eng_v}",
        "MILEAGE": f"MILEAGE+<=+{base_filers.mileage}",
        "STATUS": f"STATUS+=+'{base_filers.status}'",
        "FINISH": f"FINISH+>+{base_filers.finish}",
        "KPP_TYPE": f"KPP_TYPE+IN+(+'{ "',+'".join(kpp_types)}'+)",
    }
