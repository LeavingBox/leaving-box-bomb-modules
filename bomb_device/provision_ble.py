try:
    import ujson as json
except ImportError:
    import json

import time

try:
    import bluetooth
except ImportError:
    bluetooth = None

try:
    from .config_store import save_config
except ImportError:
    from config_store import save_config

_IRQ_CENTRAL_CONNECT = 1
_IRQ_CENTRAL_DISCONNECT = 2
_IRQ_GATTS_WRITE = 3

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_UART_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
_UART_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None

_UART_SERVICE = (
    _UART_SERVICE_UUID,
    (
        (_UART_TX_UUID, bluetooth.FLAG_NOTIFY) if bluetooth else (),
        (_UART_RX_UUID, bluetooth.FLAG_WRITE) if bluetooth else (),
    ),
)


def _advertising_payload(name: str) -> bytes:
    name_bytes = name.encode()
    payload = bytearray()
    payload += bytes((len(name_bytes) + 1, 0x09)) + name_bytes
    return payload


def _parse_payload(raw: bytes) -> dict:
    text = raw.decode().strip()
    if not text:
        return {}

    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except ValueError:
            return {}

    pairs = []
    for chunk in text.replace("\n", ";").replace("&", ";").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        pairs.append(chunk)

    result = {}
    for pair in pairs:
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        result[key.strip()] = value.strip()

    return result


class BleProvisioner:
    def __init__(self, device_name: str = "BOMB-SETUP"):
        if bluetooth is None:
            raise RuntimeError("bluetooth module is not available.")

        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._buffer = bytearray()
        self._payload = None
        self._device_name = device_name

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.discard(conn_handle)
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if value_handle != self._rx_handle:
                return
            chunk = self._ble.gatts_read(self._rx_handle)
            if not chunk:
                return
            self._buffer.extend(chunk)
            if b"\n" in self._buffer:
                line, rest = self._buffer.split(b"\n", 1)
                self._buffer = bytearray(rest)
                self._payload = line.strip()
            elif self._buffer.startswith(b"{") and self._buffer.endswith(b"}"):
                self._payload = bytes(self._buffer).strip()
                self._buffer = bytearray()

    def _advertise(self):
        self._ble.gap_advertise(100_000, adv_data=_advertising_payload(self._device_name))

    def start(self):
        self._payload = None
        self._buffer = bytearray()
        self._advertise()

    def stop(self):
        self._ble.gap_advertise(None)

    def wait_for_credentials(self, timeout_s: int = 120) -> dict:
        deadline = time.ticks_add(time.ticks_ms(), timeout_s * 1000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            if self._payload:
                data = _parse_payload(self._payload)
                if data:
                    save_config(data)
                    return data
                self._payload = None
            time.sleep_ms(50)

        raise TimeoutError("BLE provisioning timed out.")


def provision_via_ble(device_name: str = "BOMB-SETUP", timeout_s: int = 120) -> dict:
    provisioner = BleProvisioner(device_name=device_name)
    provisioner.start()
    try:
        return provisioner.wait_for_credentials(timeout_s=timeout_s)
    finally:
        provisioner.stop()
