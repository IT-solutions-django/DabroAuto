import json

from config.settings import SETTINGS_INTEGRATION_PATH


def get_settings_integration_config() -> dict:
    with open(SETTINGS_INTEGRATION_PATH) as f:
        result = json.load(f)
    return result


def save_to_json(form_data):
    with open(SETTINGS_INTEGRATION_PATH, "w", encoding="utf-8") as json_file:
        json.dump(form_data, json_file, ensure_ascii=False, indent=4)
