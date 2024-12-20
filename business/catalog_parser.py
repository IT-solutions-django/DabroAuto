from dataclasses import dataclass
from typing import Iterable, Optional
from bs4 import BeautifulSoup
import random

import requests
from django.db import transaction
from django.http import Http404

from apps.car.models import Car
from apps.catalog.models import (
    BaseFilter,
    CarMark,
    CarModel,
    Country,
    CarColorTag,
    CurrencyRate,
)
import datetime
from apps.commission.models import Commission
from business.calculate_car_price import get_config, calc_price
from config import settings


@dataclass
class CarCard:
    id: str
    mark: str
    model: str
    grade: str
    year: int
    mileage: int
    images: list[str]
    price: int
    kuzov: Optional[str] = None
    kpp: Optional[str] = None
    eng_v: Optional[str] = None
    priv: Optional[str] = None
    color: Optional[str] = None
    rate: Optional[str] = None
    finish_price: Optional[int] = None
    current_currency: Optional[CurrencyRate] = None
    commission: Optional[Commission] = None
    customs_duty: Optional[list] = None
    country: Optional[Country] = None
    equipment: Optional[str] = None
    steering_wheel: Optional[str] = None


ORDERING = {
    "asc_mileage": "+ORDER+BY+MILEAGE+ASC",
    "desc_mileage": "+ORDER+BY+MILEAGE+DESC",
    "asc_price": "+ORDER+BY+FINISH+ASC",
    "desc_price": "+ORDER+BY+FINISH+DESC",
    "asc_eng_v": "+ORDER+BY+ENG_V+ASC",
    "desc_eng_v": "+ORDER+BY+ENG_V+DESC",
    "asc_year": "+ORDER+BY+YEAR+ASC",
    "desc_year": "+ORDER+BY+YEAR+DESC",
    "asc_auc_date": "+ORDER+BY+AUCTION_DATE+ASC",
    "desc_auc_date": "+ORDER+BY+AUCTION_DATE+DESC",
}


def update_catalog_meta():
    user_ip = settings.SERVER_IP
    tables = ("stats", "main", "china")
    for table in tables:
        base_filters = get_base_filters(table)
        upload_and_save_marks_and_models(table, base_filters.values(), user_ip)


def get_car_by_id(country_manufacturing: str, car_id: str, user_ip: str):
    try:
        car = Car.objects.get(
            id=car_id, country_manufacturing__name=country_manufacturing
        )
    except Exception:
        car = None

    if car is not None:
        return CarCard(
            id=str(car.id),
            mark=car.brand.name,
            model=car.model.name,
            grade=car.specification,
            year=car.year_manufactured,
            mileage=car.mileage,
            price=car.price,
            images=["/media/" + im.image.name for im in car.image.all()],
            kuzov=car.kuzov,
            kpp=car.kpp,
            eng_v=str(car.eng_v).replace(",", "."),
            priv=car.priv,
            color=car.color,
        ), True

    country = Country.objects.get(name=country_manufacturing)

    query = get_sql_query(
        "*",
        country.table_name,
        [f"id+=+'{car_id}'"],
        "0,1",
    )
    data = fetch_by_query(query, user_ip)

    try:
        car = data[0]
    except Exception:
        raise Http404()

    if car["PRIV"] == "FF":
        priv = "Передний привод"
    elif car["PRIV"] == "FR":
        priv = "Задний привод"
    else:
        priv = "Полный привод"

    color_tag = CarColorTag.objects.filter(name=car["COLOR"]).first()

    config = get_config()
    commission = Commission.objects.get(country=country)
    curr = {
        "jpy": float(CurrencyRate.objects.get(name="Иена").course),
        "eur": float(CurrencyRate.objects.get(name="Евро").course),
        "cny": float(CurrencyRate.objects.get(name="Юань").course),
        "kor": float(CurrencyRate.objects.get(name="Вона").course),
    }

    current_currency = get_current_currency(country)

    images = [image for image in car["IMAGES"].split("#")]
    images = [*images[1:], images[0]]

    car_rate = car.get('RATE', '')
    if car_rate:
        car_rate = car['RATE']

    return CarCard(
        id=car["ID"],
        mark=car["MARKA_NAME"],
        model=car["MODEL_NAME"],
        grade=car["GRADE"],
        year=car["YEAR"],
        mileage=car["MILEAGE"],
        price=int(
            calc_price(
                car["FINISH"],
                curr,
                car["YEAR"],
                car["ENG_V"],
                country.table_name,
                config,
                commission,
            )[0]
        ),
        images=images,
        kuzov=car["KUZOV"],
        kpp="Механика" if car["KPP_TYPE"] == 1 else "Автомат",
        eng_v=str(float(car["ENG_V"]) / 1000),
        priv=priv,
        color=color_tag.color.name if color_tag is not None else car["COLOR"],
        rate=car_rate if car_rate else None,
        finish_price=int(car["FINISH"]),
        commission=commission,
        current_currency=current_currency,
        customs_duty=calc_price(
            car["FINISH"],
            curr,
            car["YEAR"],
            car["ENG_V"],
            country.table_name,
            config,
            commission,
        )[1],
        country=country
    ), False


def get_current_currency(country: Country) -> CurrencyRate:
    if country.name == "Япония":
        return CurrencyRate.objects.get(name="Иена")
    elif country.name == "Китай":
        return CurrencyRate.objects.get(name="Юань")
    else:
        return CurrencyRate.objects.get(name="Вона")


def get_popular_cars(country_manufacturing: str, count_cars: int):
    cars = list(
        Car.objects.filter(
            country_manufacturing__name=country_manufacturing, is_popular=True
        )
    )

    random.shuffle(cars)

    return cars[:count_cars]


def get_cars_info(
        table_name: str, filters: dict, page: str, cars_per_page: int, user_ip: str
):
    base_filters = get_base_filters(table_name)
    ordering = get_ordering(filters)
    filters = connect_filters(filters, base_filters)

    query = get_sql_query(
        "*",
        table_name,
        filters,
        f"{cars_per_page * (int(page) - 1)},{cars_per_page}",
        ordering,
    )
    print(query)
    data = fetch_by_query(query, user_ip)

    config = get_config()
    commission = Commission.objects.get(country__table_name=table_name)
    curr = {
        "jpy": float(CurrencyRate.objects.get(name="Иена").course),
        "eur": float(CurrencyRate.objects.get(name="Евро").course),
        "cny": float(CurrencyRate.objects.get(name="Юань").course),
        "kor": float(CurrencyRate.objects.get(name="Вона").course),
    }

    clear_data = [
        CarCard(
            id=car["ID"],
            mark=car["MARKA_NAME"],
            model=car["MODEL_NAME"],
            grade=car["GRADE"],
            year=car["YEAR"],
            mileage=car["MILEAGE"],
            eng_v=str(float(car["ENG_V"]) / 1000),
            price=int(
                calc_price(
                    car["FINISH"],
                    curr,
                    car["YEAR"],
                    car["ENG_V"],
                    table_name,
                    config,
                    commission,
                )[0]
            ),
            images=[image[:-3] for image in car["IMAGES"].split("#")],
            rate=car["RATE"],
            priv=(
                "Передний" if car["PRIV"] == "FF" else
                "Задний" if car["PRIV"] == "FR" else
                "Полный"
            )
        )
        for car in data
    ]

    cars_count = get_cars_count(table_name, filters, user_ip)
    pages_count = (int(cars_count) - 1) // cars_per_page + 1

    return clear_data, pages_count


def get_ordering(filters: dict):
    ordering = filters.get("ordering") or ""

    return ORDERING.get(ordering, "")


def get_cars_count(table_name: str, filters: list[str], user_ip: str):
    query = get_sql_query(
        "count(*)",
        table_name,
        filters,
        "0,1",
    )
    data = fetch_by_query(query, user_ip)
    return data[0]["TAG0"]


def connect_filters(filters: dict, base_filters: dict):
    mark_name = get_model_data_or_none(filters.get("mark"), CarMark)
    model_name = get_model_data_or_none(filters.get("model"), CarModel)
    priv = filters.get("priv") or None
    colors = get_color_data_or_none(filters.get("color")) or None
    year_from = filters.get("year_from") or None
    year_to = filters.get("year_to") or None
    eng_v_from = filters.get("eng_v_from") or None
    eng_v_to = filters.get("eng_v_to") or None
    mileage_from = filters.get("mileage_from") or None
    mileage_to = filters.get("mileage_to") or None
    kpp_type = filters.get("kpp_type") or None
    rate = filters.get("rate") or None

    excluded_priv = base_filters.get("PRIV") and "," + base_filters["PRIV"][13:-1]

    if priv in ("FF", "FR"):
        priv = f"PRIV+=+'{priv}'"
    elif priv == "NOT":
        priv = f"PRIV+NOT+IN+('FF',+'FR'{excluded_priv or ''})"

    result = [
        mark_name and f"MARKA_NAME+=+'{mark_name}'",
        model_name and f"MODEL_NAME+=+'{model_name}'",
        priv,
        colors and f"COLOR+IN+(+'{"',+'".join(colors)}'+)",
        year_from and f"YEAR+>=+{year_from}",
        year_to and f"YEAR+<=+{year_to}",
        eng_v_from and f"ENG_V+>=+{eng_v_from}",
        eng_v_to and f"ENG_V+<=+{eng_v_to}",
        mileage_from and f"MILEAGE+>=+{mileage_from}",
        mileage_to and f"MILEAGE+<=+{mileage_to}",
        kpp_type and f"KPP_TYPE+=+'{kpp_type}'",
        rate and f"RATE+IN+(+'{rate}'+)",
    ]

    if mark_name is not None:
        del base_filters["MARKA_NAME"]

    if year_from:
        del base_filters["YEAR"]

    if eng_v_from:
        del base_filters["ENG_V"]

    if eng_v_to:
        del base_filters["MAX_ENG_V"]

    if mileage_to:
        del base_filters["MILEAGE"]

    if kpp_type:
        del base_filters["KPP_TYPE"]

    if priv and base_filters.get("PRIV"):
        del base_filters["PRIV"]

    if rate:
        del base_filters["RATE"]

    result.extend(base_filters.values())

    result = [res for res in result if res is not None]

    return result


def get_model_data_or_none(id: str | None, model):
    try:
        return model.objects.get(id=id).name
    except:
        return None


def get_color_data_or_none(id: str | None):
    try:
        tags = CarColorTag.objects.filter(color_id=id)
        return [tag.name for tag in tags]
    except:
        return None


@transaction.atomic
def upload_and_save_marks_and_models(
        table_name: str, base_filters: Iterable[str], user_ip: str
):
    country_manufacturing = Country.objects.get(table_name=table_name)
    CarMark.objects.filter(country_manufacturing=country_manufacturing).delete()
    CarModel.objects.filter(mark__country_manufacturing=country_manufacturing).delete()

    fields = "DISTINCT+MODEL_NAME,+MARKA_NAME"

    for line in full_data_fetch(fields, table_name, base_filters, user_ip):
        car_mark, _ = CarMark.objects.get_or_create(
            name=line["MARKA_NAME"], country_manufacturing=country_manufacturing
        )
        CarModel.objects.create(name=line["MODEL_NAME"], mark=car_mark)


def full_data_fetch(
        fields: str, table_name: str, base_filters: Iterable[str], user_ip: str
):
    offset = 0
    query = get_sql_query(fields, table_name, base_filters, f"{offset},250")
    data = fetch_by_query(query, user_ip)

    while len(data) > 0:
        yield from data

        offset += 250
        query = get_sql_query(fields, table_name, base_filters, f"{offset},250")
        data = fetch_by_query(query, user_ip)


def fetch_by_query(sql_query: str, user_ip: str):
    url = f"http://78.46.90.228/api/?ip={user_ip}&code=A25nhGfE56Kd&sql={sql_query}"
    res = requests.get(url)
    soup = BeautifulSoup(res.content.decode("utf-8"), "xml")
    return [
        {elem.name: elem.getText() for elem in row.findChildren()}
        for row in soup.findAll("row")
    ]


def get_sql_query(
        fields: str,
        table_name: str,
        base_filters: Iterable[str],
        limit: str,
        ordering: str = "",
):
    query = f"select+{fields}+from+{table_name}+WHERE+1+=+1+and+{'+and+'.join(base_filters)}{ordering}+limit+{limit}"
    return query


def get_base_filters(table_name: str):
    base_filers = BaseFilter.objects.get(country_manufacturing__table_name=table_name)

    max_auction_date = (
            base_filers.auction_date
            and datetime.datetime.now()
            - datetime.timedelta(days=int(base_filers.auction_date))
    )

    kpp_types = (str(kpp_type) for kpp_type in base_filers.kpp_type)

    result = {
        "AUCTION": f"AUCTION+NOT+LIKE+'%{base_filers.auction}%'",
        "MARKA_NAME": f"MARKA_NAME+NOT+IN+(+'{"',+'".join(base_filers.marka_name)}'+)",
        "YEAR": f"YEAR+>=+{base_filers.year}",
        "ENG_V": f"ENG_V+>+{base_filers.eng_v}",
        "MAX_ENG_V": f"ENG_V+<=+{base_filers.max_eng_v * 1000}",
        "MILEAGE": f"MILEAGE+<=+{base_filers.mileage}",
        "FINISH": f"FINISH+>+{base_filers.finish}",
        "KPP_TYPE": f"KPP_TYPE+IN+(+'{"',+'".join(kpp_types)}'+)",
    }
    if base_filers.auction_date is not None:
        result.update(
            {
                "AUCTION_DATE": f"AUCTION_DATE+>=+'{max_auction_date.date()}'",
            }
        )

    if base_filers.status is not None:
        result.update(
            {
                "STATUS": f"STATUS+=+'{base_filers.status}'",
            }
        )

    if base_filers.priv:
        result.update(
            {
                "PRIV": f"PRIV+NOT+IN+(+'{"',+'".join(base_filers.priv)}'+)",
            }
        )

    if base_filers.rate:
        result.update(
            {
                "RATE": f"RATE+IN+(+'{"',+'".join(base_filers.rate)}'+)",
            }
        )

    return result
