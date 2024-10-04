from typing import Iterable
import xml.etree.ElementTree as ET

import requests
from django.db import transaction

from src.apps.catalog.models import BaseFilter, CarMark, CarModel
import datetime


def construct_query_with_base_filters():
    base_filters = get_base_filters()
    upload_and_save_marks_and_models(base_filters)


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


def get_base_filters():
    auction_date = BaseFilter.objects.get(model_name="AUCTION_DATE").content
    auction = BaseFilter.objects.get(model_name="AUCTION").content
    marka_name = BaseFilter.objects.get(model_name="MARKA_NAME").content
    year = BaseFilter.objects.get(model_name="YEAR").content
    eng_v = BaseFilter.objects.get(model_name="ENG_V").content
    mileage = BaseFilter.objects.get(model_name="MILEAGE").content
    status = BaseFilter.objects.get(model_name="STATUS").content
    finish = BaseFilter.objects.get(model_name="FINISH").content
    kpp_type = BaseFilter.objects.get(model_name="KPP_TYPE").content

    max_auction_date = datetime.datetime.now() - datetime.timedelta(
        days=int(auction_date)
    )

    return {
        "AUCTION_DATE": f"AUCTION_DATE+>=+'{max_auction_date.date()}'",
        "AUCTION": f"AUCTION+NOT+LIKE+'%{auction}%'",
        "MARKA_NAME": f"MARKA_NAME+NOT+IN+(+'{ "',+'".join(marka_name.split(';'))}'+)",
        "YEAR": f"YEAR+<=+{year}",
        "ENG_V": f"ENG_V+>+{eng_v}",
        "MILEAGE": f"MILEAGE+<=+{mileage}",
        "STATUS": f"STATUS+=+'{status}'",
        "FINISH": f"FINISH+>+{finish}",
        "KPP_TYPE": f"KPP_TYPE+IN+(+'{ "',+'".join(kpp_type.split(';'))}'+)",
    }
