try:
    import ujson as json
except ImportError:
    import json

try:
    import uos as os
except ImportError:
    import os

CONFIG_PATH = "config.json"
BLE_INFO_PATH = "ble_info.json"
REQUIRED_FIELDS = ("ssid", "session_code")
DEFAULTS = {
    "ssid": "",
    "password": "",
    "session_code": "",
    "tcp_host": "",
    "tcp_port": 3200,
    "tcp_timeout_s": 5,
    "tcp_poll_interval_ms": 500,
    "tcp_connect_retry_ms": 5000,
    "tcp_state_log_interval_ms": 5000,
    "tcp_debug": True,
    "tcp_trace": False,
    "heartbeat_s": 5,
    "wifi_timeout_s": 15,
    "broadcast_interval_ms": 200,
    "loop_delay_ms": 50,
    "provision_timeout_s": 120,
    "ble_device_name": "BOMB-SETUP",
}


def _to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_bool(value, default):
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("1", "true", "yes", "y", "on"):
            return True
        if text in ("0", "false", "no", "n", "off"):
            return False
    return default


def _to_str(value):
    if value is None:
        return ""
    return str(value)


def _apply_defaults(config: dict) -> dict:
    merged = DEFAULTS.copy()
    if config:
        for key in config:
            merged[key] = config[key]

    merged["ssid"] = _to_str(merged.get("ssid", "")).strip()
    merged["password"] = _to_str(merged.get("password", ""))
    merged["session_code"] = _to_str(merged.get("session_code", "")).strip().upper()

    merged["tcp_host"] = _to_str(merged.get("tcp_host", "")).strip() or DEFAULTS["tcp_host"]
    merged["tcp_port"] = _to_int(merged.get("tcp_port"), DEFAULTS["tcp_port"])
    merged["tcp_timeout_s"] = _to_int(merged.get("tcp_timeout_s"), DEFAULTS["tcp_timeout_s"])
    merged["tcp_poll_interval_ms"] = _to_int(
        merged.get("tcp_poll_interval_ms"), DEFAULTS["tcp_poll_interval_ms"]
    )
    merged["tcp_connect_retry_ms"] = _to_int(
        merged.get("tcp_connect_retry_ms"), DEFAULTS["tcp_connect_retry_ms"]
    )
    merged["tcp_state_log_interval_ms"] = _to_int(
        merged.get("tcp_state_log_interval_ms"), DEFAULTS["tcp_state_log_interval_ms"]
    )
    merged["tcp_debug"] = _to_bool(merged.get("tcp_debug"), DEFAULTS["tcp_debug"])
    merged["tcp_trace"] = _to_bool(merged.get("tcp_trace"), DEFAULTS["tcp_trace"])
    merged["heartbeat_s"] = _to_int(merged.get("heartbeat_s"), DEFAULTS["heartbeat_s"])
    merged["wifi_timeout_s"] = _to_int(merged.get("wifi_timeout_s"), DEFAULTS["wifi_timeout_s"])
    merged["broadcast_interval_ms"] = _to_int(
        merged.get("broadcast_interval_ms"), DEFAULTS["broadcast_interval_ms"]
    )
    merged["loop_delay_ms"] = _to_int(
        merged.get("loop_delay_ms"), DEFAULTS["loop_delay_ms"]
    )
    return merged


def _is_alnum(text: str) -> bool:
    for ch in text:
        if "0" <= ch <= "9" or "A" <= ch <= "Z" or "a" <= ch <= "z":
            continue
        return False
    return True


def _is_valid_session_code(code: str) -> bool:
    return len(code) == 6 and _is_alnum(code)


def _validate_config(config: dict) -> None:
    for key in REQUIRED_FIELDS:
        if key not in config or not str(config[key]).strip():
            raise ValueError("Missing required field: %s" % key)

    if not _is_valid_session_code(str(config["session_code"])):
        raise ValueError("Session code must be 6 alphanumeric characters.")


def save_config(config: dict) -> None:
    data = {}
    if config_exists():
        data.update(load_config())
    if config:
        data.update(config)
    data = _apply_defaults(data)
    _validate_config(data)

    with open(CONFIG_PATH, "w") as handle:
        handle.write(json.dumps(data))


def load_config() -> dict:
    if not config_exists():
        return {}

    with open(CONFIG_PATH, "r") as handle:
        return _apply_defaults(json.loads(handle.read()))


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


def save_ble_info(info: dict) -> None:
    if not info:
        return
    try:
        with open(BLE_INFO_PATH, "w") as handle:
            handle.write(json.dumps(info))
    except OSError:
        pass


def load_ble_info() -> dict:
    try:
        os.stat(BLE_INFO_PATH)
    except OSError:
        return {}

    try:
        with open(BLE_INFO_PATH, "r") as handle:
            return json.loads(handle.read())
    except OSError:
        return {}
