try:
    import network
except ImportError:
    network = None

import time


def connect_wifi(ssid: str, password: str, timeout_s: int = 15) -> bool:
    if network is None:
        raise RuntimeError("network module is not available.")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return True

    wlan.connect(ssid, password)
    deadline = time.ticks_add(time.ticks_ms(), timeout_s * 1000)
    while not wlan.isconnected():
        if time.ticks_diff(deadline, time.ticks_ms()) <= 0:
            return False
        time.sleep_ms(200)
    return True


def get_mac() -> bytes:
    if network is None:
        raise RuntimeError("network module is not available.")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.config("mac")