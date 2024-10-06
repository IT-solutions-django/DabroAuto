from typing import Iterable
import xml.etree.ElementTree as ET

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
    xml_node = ET.fromstring(res.text)

    return [{elem.tag: elem.text for elem in row} for row in xml_node.findall("row")]


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
