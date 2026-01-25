try:
    from .config_store import save_config
    from .provision_ble import provision_via_ble
    from .provision_http import provision_via_http
except ImportError:
    from config_store import save_config
    from provision_ble import provision_via_ble
    from provision_http import provision_via_http


def provision(
    mode: str,
    timeout_s: int = 120,
    ap_ssid: str = "BOMB-SETUP",
    ap_password: str = "",
    port: int = 8080,
    device_name: str = "BOMB-SETUP",
) -> dict:
    mode = (mode or "").lower().strip()
    if mode == "http":
        return provision_via_http(
            ap_ssid=ap_ssid,
            ap_password=ap_password,
            port=port,
            timeout_s=timeout_s,
        )
    if mode == "ble":
        return provision_via_ble(device_name=device_name, timeout_s=timeout_s)
    raise ValueError("Unknown provisioning mode: %s" % mode)


def provision_both(
    timeout_s: int = 120,
    ap_ssid: str = "BOMB-SETUP",
    ap_password: str = "",
    port: int = 8080,
    device_name: str = "BOMB-SETUP",
) -> dict:
    try:
        return provision_via_ble(device_name=device_name, timeout_s=timeout_s)
    except Exception:
        pass

    return provision_via_http(
        ap_ssid=ap_ssid,
        ap_password=ap_password,
        port=port,
        timeout_s=timeout_s,
    )


def save_manual(ssid: str, password: str, session_code: str) -> None:
    save_config(
        {
            "ssid": ssid,
            "password": password,
            "session_code": session_code,
        }
    )
