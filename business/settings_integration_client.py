import json

from config.settings import SETTINGS_INTEGRATION_PATH


def get_settings_integration_config() -> dict:
    with open(SETTINGS_INTEGRATION_PATH) as f:
        result = json.load(f)
    return result
