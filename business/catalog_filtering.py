from typing import Iterable
import xml.etree.ElementTree as ET

import requests
from django.db import transaction

from apps.catalog.models import BaseFilter, CarMark, CarModel, CarColor
import datetime


def construct_query_with_base_filters():
    table_name = "stats"
    base_filters = get_base_filters(table_name)
    upload_and_save_marks_and_models(base_filters)
    upload_and_save_colors(base_filters)


@transaction.atomic
def upload_and_save_colors(base_filters: dict[str, str]):
    CarColor.objects.all().delete()

    limit_start = 0
    query = get_sql_query("DISTINCT+COLOR", base_filters.values(), f"{limit_start},250")
    data = fetch_by_query(query)

    while len(data) > 0:
        for row in data:
            if row.get("COLOR") is None:
                continue
            print(row)
            CarColor.objects.create(name=row["COLOR"])

        limit_start += 250
        query = get_sql_query(
            "DISTINCT+MODEL_NAME,+MARKA_NAME",
            base_filters.values(),
            f"{limit_start},250",
        )
        data = fetch_by_query(query)


@transaction.atomic
def upload_and_save_marks_and_models(base_filters: dict[str, str]):

    CarMark.objects.all().delete()
    CarModel.objects.all().delete()

    limit_start = 0
    query = get_sql_query(
        "DISTINCT+MODEL_NAME,+MARKA_NAME", base_filters.values(), f"{limit_start},250"
    )
    data = fetch_by_query(query)

    while len(data) > 0:
        for row in data:
            print(row)
            car_mark, _ = CarMark.objects.get_or_create(name=row["MARKA_NAME"])
            CarModel.objects.create(name=row["MODEL_NAME"], mark=car_mark)

        limit_start += 250
        query = get_sql_query(
            "DISTINCT+MODEL_NAME,+MARKA_NAME",
            base_filters.values(),
            f"{limit_start},250",
        )
        data = fetch_by_query(query)


def fetch_by_query(sql_query: str):
    url = f"http://78.46.90.228/api/?ip=45.84.177.55&code=A25nhGfE56Kd&sql={sql_query}"
    res = requests.get(url)
    xml_node = ET.fromstring(res.text)

    result = []

    for row in xml_node.findall("row"):
        result_dict = {}
        for elem in row:
            result_dict[elem.tag] = elem.text
        result.append(result_dict)

    return result


def get_sql_query(fields: str, base_filters: Iterable[str], limit: str):
    query = f"select+{fields}+from+stats+WHERE+1+=+1+and+{'+and+'.join(base_filters)}+limit+{limit}"
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
