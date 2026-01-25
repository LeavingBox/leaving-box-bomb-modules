try:
    import espnow
    import network
except ImportError:
    espnow = None
    network = None


class EspNowBus:
    def __init__(self):
        self._wlan = None
        self._espnow = None

    def init(self):
        if espnow is None or network is None:
            raise RuntimeError("ESP-NOW is not available in this environment.")

        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        self._espnow = espnow.ESPNow()
        self._espnow.active(True)

    def add_peer(self, mac: bytes):
        if not self._espnow:
            raise RuntimeError("ESP-NOW not initialized.")
        try:
            self._espnow.add_peer(mac)
        except OSError:
            # Peer may already be added.
            pass

    def del_peer(self, mac: bytes):
        if not self._espnow:
            raise RuntimeError("ESP-NOW not initialized.")
        try:
            self._espnow.del_peer(mac)
        except OSError:
            pass

    def send(self, mac: bytes, payload: bytes, sync: bool = False) -> bool:
        if not self._espnow:
            raise RuntimeError("ESP-NOW not initialized.")
        try:
            self._espnow.send(mac, payload, sync)
            return True
        except OSError:
            return False

    def recv(self, timeout_ms: int = 0):
        if not self._espnow:
            raise RuntimeError("ESP-NOW not initialized.")
        return self._espnow.recv(timeout_ms)


class NullEspNowBus:
    def init(self):
        return None

    def add_peer(self, mac: bytes):
        return None

    def del_peer(self, mac: bytes):
        return None

    def send(self, mac: bytes, payload: bytes, sync: bool = False) -> bool:
        return True

    def recv(self, timeout_ms: int = 0):
        return None, None
