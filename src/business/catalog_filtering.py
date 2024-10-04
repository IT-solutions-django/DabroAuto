from src.apps.catalog.models import BaseFilter
import datetime


def construct_query_with_base_filters():
    # base_filters = get_base_filters()
    # query = get_sql_query(base_filters)
    # print(query)
    upload_and_save_marks_and_models()


def upload_and_save_marks_and_models():
    base_filters = get_base_filters()
    query = get_sql_query("DISTINCT+MODEL_NAME,+MARKA_NAME", base_filters, "0,250")
    print(query)


def get_sql_query(fields: str, base_filters: dict, limit: str):
    query = f"select+{fields}+from+stats+WHERE+1+=+1+and+{ '+and+'.join(base_filters.values())  }+limit+{limit}"
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

    # max_auction_date = datetime.datetime.now() - datetime.timedelta(
    #     days=int(auction_date)
    # )
    max_auction_date = datetime.datetime.now() - datetime.timedelta(days=1)

    return {
        "AUCTION_DATE": f"AUCTION_DATE+>=+'{max_auction_date.date()}'",
        "AUCTION": f"AUCTION+NOT+LIKE+%22%{auction}%%22",
        "MARKA_NAME": f"MARKA_NAME+NOT+IN+(+'{ "',+'".join(marka_name.split(';'))}'+)",
        "YEAR": f"YEAR+<=+{year}",
        "ENG_V": f"ENG_V+>+{eng_v}",
        "MILEAGE": f"MILEAGE+<=+{mileage}",
        "STATUS": f"STATUS+=+'{status}'",
        "FINISH": f"FINISH+>+{finish}",
        "KPP_TYPE": f"KPP_TYPE+IN+(+'{ "',+'".join(kpp_type.split(';'))}'+)",
    }
