from datetime import datetime

TABLE_SETTINGS = {
    "stats": {"commission": 0, "currency": "jpy"},
    "china": {"commission": 0, "currency": "cny"},
    "main": {"commission": 0, "currency": "kor"},
}

CARS_TOF = [
    {"price_interval": (0, 200000), "tof": 775},
    {"price_interval": (200000, 450000), "tof": 1550},
    {"price_interval": (450000, 1200000), "tof": 3100},
    {"price_interval": (1200000, 2700000), "tof": 8530},
    {"price_interval": (2700000, 4200000), "tof": 12000},
    {"price_interval": (4200000, 5500000), "tof": 15550},
    {"price_interval": (5500000, 7000000), "tof": 20000},
    {"price_interval": (7000000, 8000000), "tof": 23000},
    {"price_interval": (8000000, 9000000), "tof": 25000},
    {"price_interval": (9000000, 10000000), "tof": 27000},
    {"price_interval": (10000000, float("inf")), "tof": 30000},
]

NEW_CARS_DUTY = [
    {
        "price_interval": (0, 8500),
        "multiplier": 0.54,
        "min_by_eng_v": 2.5,
    },
    {
        "price_interval": (8500, 16700),
        "multiplier": 0.48,
        "min_by_eng_v": 3.5,
    },
    {
        "price_interval": (16700, 42300),
        "multiplier": 0.48,
        "min_by_eng_v": 5.5,
    },
    {
        "price_interval": (42300, 84500),
        "multiplier": 0.48,
        "min_by_eng_v": 7.5,
    },
    {
        "price_interval": (84500, 169000),
        "multiplier": 0.48,
        "min_by_eng_v": 15,
    },
    {
        "price_interval": (169000, float("inf")),
        "multiplier": 0.48,
        "min_by_eng_v": 20,
    },
]

OLD_CARS_DUTY = [
    {
        "volume_interval": (0, 1000),
        "multiplier": 1.5,
        "age_interval": (3, 5),
    },
    {
        "volume_interval": (1000, 1500),
        "multiplier": 1.7,
        "age_interval": (3, 5),
    },
    {
        "volume_interval": (1500, 1800),
        "multiplier": 2.5,
        "age_interval": (3, 5),
    },
    {
        "volume_interval": (1800, 2300),
        "multiplier": 2.7,
        "age_interval": (3, 5),
    },
    {
        "volume_interval": (2300, 3000),
        "multiplier": 3,
        "age_interval": (3, 5),
    },
    {
        "volume_interval": (3000, float("inf")),
        "multiplier": 3.6,
        "age_interval": (3, 5),
    },
    {
        "volume_interval": (0, 1000),
        "multiplier": 3,
        "age_interval": (5, float("inf")),
    },
    {
        "volume_interval": (1000, 1500),
        "multiplier": 3.2,
        "age_interval": (5, float("inf")),
    },
    {
        "volume_interval": (1500, 1800),
        "multiplier": 3.5,
        "age_interval": (5, float("inf")),
    },
    {
        "volume_interval": (1800, 2300),
        "multiplier": 4.8,
        "age_interval": (5, float("inf")),
    },
    {
        "volume_interval": (2300, 3000),
        "multiplier": 5,
        "age_interval": (5, float("inf")),
    },
    {
        "volume_interval": (3000, float("inf")),
        "multiplier": 5.7,
        "age_interval": (5, float("inf")),
    },
]

CARS_YTS = [
    {
        "age_interval": (0, 3),
        "volume_interval": (3500, float("inf")),
        "yts": 2285200,
    },
    {
        "age_interval": (0, 3),
        "volume_interval": (3000, 3500),
        "yts": 1794600,
    },
    {
        "age_interval": (0, 3),
        "volume_interval": (0, 3000),
        "yts": 3400,
    },
    {
        "age_interval": (3, float("inf")),
        "volume_interval": (3500, float("inf")),
        "yts": 3004000,
    },
    {
        "age_interval": (3, float("inf")),
        "volume_interval": (3000, 3500),
        "yts": 2747200,
    },
    {
        "age_interval": (3, float("inf")),
        "volume_interval": (0, 3000),
        "yts": 5200,
    },
]


def get_tof(price: int):
    for interval in CARS_TOF:
        if interval["price_interval"][0] < price <= interval["price_interval"][1]:
            return interval["tof"]


def get_new_cars_duty(price_eur: float, volume: int, currency_eur: float):
    volume = float(volume)

    for duty_info in NEW_CARS_DUTY:
        if duty_info["price_interval"][0] <= price_eur < duty_info["price_interval"][1]:
            duty = price_eur * duty_info["multiplier"]
            if float(duty) / volume < duty_info["min_by_eng_v"]:
                duty = volume * duty_info["min_by_eng_v"]
            return duty * currency_eur


def get_old_car_duty(volume: int, age: int, currency_eur: float):
    for duty_info in OLD_CARS_DUTY:
        if (
            duty_info["age_interval"][0] <= age < duty_info["age_interval"][1]
            and duty_info["volume_interval"][0]
            < volume
            <= duty_info["volume_interval"][1]
        ):
            duty = volume * duty_info["multiplier"]
            return duty * currency_eur


def get_yts(age: int, volume: int):
    for yts_info in CARS_YTS:
        if (
            yts_info["age_interval"][0] <= age < yts_info["age_interval"][1]
            and yts_info["volume_interval"][0]
            <= volume
            < yts_info["volume_interval"][1]
        ):
            return yts_info["yts"]


def calc_price(price, currency, year, volume, table):
    try:
        commission = TABLE_SETTINGS[table]["commission"]
        one_rub = currency[TABLE_SETTINGS[table]["currency"]]

        price_rus = round(price / one_rub)
        price_eur = float(price_rus) / currency["eur"]

        age = datetime.now().year - year

        tof = get_tof(price_rus)

        if age < 3:
            duty = get_new_cars_duty(price_eur, volume, currency["eur"])
        else:
            duty = get_old_car_duty(volume, age, currency["eur"])

        yts = get_yts(age, volume)

        toll = duty + tof + yts + commission

        full_price = toll + price_rus

        return full_price, toll
    except Exception as e:
        print(e)


curr = {
    "jpy": 1.5352,
    "eur": 106.5074,
    "cny": 0.073,
    "kor": 1.38606,
}


c = calc_price(
    21800,
    curr,
    2021,
    4300,
    "stats",
)
print(c)
