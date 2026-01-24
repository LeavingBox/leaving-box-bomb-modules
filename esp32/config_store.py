try:
    import ujson as json
except ImportError:
    import json

try:
    import uos as os
except ImportError:
    import os

CONFIG_PATH = "config.json"
REQUIRED_FIELDS = ("ssid", "password", "session_code")


def _is_valid_session_code(code: str) -> bool:
    return len(code) == 6 and code.isalnum()


def _validate_config(config: dict) -> None:
    for key in REQUIRED_FIELDS:
        if key not in config or not str(config[key]).strip():
            raise ValueError("Missing required field: %s" % key)

    if not _is_valid_session_code(str(config["session_code"])):
        raise ValueError("Session code must be 6 alphanumeric characters.")


def save_config(config: dict) -> None:
    data = {
        "ssid": str(config.get("ssid", "")).strip(),
        "password": str(config.get("password", "")).strip(),
        "session_code": str(config.get("session_code", "")).strip(),
    }
    _validate_config(data)

    with open(CONFIG_PATH, "w") as handle:
        handle.write(json.dumps(data))


def load_config() -> dict:
    if not config_exists():
        return {}

    with open(CONFIG_PATH, "r") as handle:
        return json.loads(handle.read())


def config_exists() -> bool:
    try:
        os.stat(CONFIG_PATH)
        return True
    except OSError:
        return False


def clear_config() -> None:
    try:
        os.remove(CONFIG_PATH)
    except OSError:
        pass
