try:
    from .config_store import save_config
    from .provision_ble import provision_via_ble
except ImportError:
    from config_store import save_config
    from provision_ble import provision_via_ble


def provision(
    mode: str,
    timeout_s: int = 120,
    device_name: str = "BOMB-SETUP",
) -> dict:
    mode = (mode or "").lower().strip()
    if mode == "http":
        print("Provisioning via HTTP...???")
    if mode == "ble":
        print("Provisioning via BLE...")
        return provision_via_ble(device_name=device_name, timeout_s=timeout_s)
    raise ValueError("Unknown provisioning mode: %s" % mode)


def provision_both(
    timeout_s: int = 120,
    device_name: str = "BOMB-SETUP",
) -> dict:
    try:
        return provision_via_ble(device_name=device_name, timeout_s=timeout_s)
    except Exception:
        pass

    print("Provisioning via HTTP...???")


def save_manual(ssid: str, password: str, session_code: str) -> None:
    save_config(
        {
            "ssid": ssid,
            "password": password,
            "session_code": session_code,
        }
    )
