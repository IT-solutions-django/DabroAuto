import json
from datetime import datetime


def get_tof(price: int, cars_tof: list[dict]):
    for interval in cars_tof:
        if (
            interval["price_interval"][0]
            < price
            <= float(interval["price_interval"][1])
        ):
            return interval["tof"]


def get_new_cars_duty(
    price_eur: float, volume: int, currency_eur: float, new_cars_duty: list[dict]
):
    volume = float(volume)

    for duty_info in new_cars_duty:
        if (
            duty_info["price_interval"][0]
            <= price_eur
            < float(duty_info["price_interval"][1])
        ):
            duty = price_eur * duty_info["multiplier"]
            if float(duty) / volume < duty_info["min_by_eng_v"]:
                duty = volume * duty_info["min_by_eng_v"]
            return duty * currency_eur


def get_old_car_duty(
    volume: int, age: int, currency_eur: float, old_cars_duty: list[dict]
):
    for duty_info in old_cars_duty:
        if duty_info["age_interval"][0] <= age < float(
            duty_info["age_interval"][1]
        ) and duty_info["volume_interval"][0] < volume <= float(
            duty_info["volume_interval"][1]
        ):
            duty = volume * duty_info["multiplier"]
            return duty * currency_eur


def get_yts(age: int, volume: int, cars_yts: list[dict]):
    for yts_info in cars_yts:
        if yts_info["age_interval"][0] <= age < float(
            yts_info["age_interval"][1]
        ) and yts_info["volume_interval"][0] < volume <= float(
            yts_info["volume_interval"][1]
        ):
            return yts_info["yts"]


def calc_price(price, currency, year, volume, table):
    try:
        with open("config/calculating_car_price_config.json") as f:
            conf = json.load(f)

        commission = conf["table_settings"][table]["commission"]
        one_rub = currency[conf["table_settings"][table]["currency"]]

        price_rus = round(price / one_rub)
        price_eur = float(price_rus) / currency["eur"]

        age = datetime.now().year - year

        tof = get_tof(price_rus, conf["car_tof"])

        if age < 3:
            duty = get_new_cars_duty(
                price_eur, volume, currency["eur"], conf["new_cars_duty"]
            )
        else:
            duty = get_old_car_duty(volume, age, currency["eur"], conf["old_cars_duty"])

        yts = get_yts(age, volume, conf["cars_yts"])

        toll = duty + tof + yts + commission

        full_price = toll + price_rus
        return round(full_price, 2), round(toll, 2)
    except Exception as e:
        print(e)


curr = {
    "jpy": 1.55,
    "eur": 105.1095,
    "cny": 0.07421,
    "kor": 14.05,
}

c = calc_price(
    1429000,
    curr,
    2016,
    3500,
    "main",
)
print(c)
