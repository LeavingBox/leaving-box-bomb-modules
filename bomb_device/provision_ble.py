import time

try:
    import uasyncio as asyncio
except ImportError:
    asyncio = None
try:
    import gc
except ImportError:
    gc = None

try:
    TimeoutError
except NameError:
    class TimeoutError(Exception):
        pass

try:
    import bluetooth
except ImportError:
    bluetooth = None

try:
    import aioble
except ImportError:
    aioble = None

try:
    from .config_store import save_ble_info, save_config
    from .ble.receiver import BleCredentialReceiver
except ImportError:
    from config_store import save_ble_info, save_config
    from ble.receiver import BleCredentialReceiver

_UART_SERVICE_UUID = (
    bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
)
_UART_RX_UUID = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
)
_UART_TX_UUID = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E") if bluetooth else None
)


class BleProvisioner:
    def __init__(
        self,
        device_name: str = "BOMB-SETUP",
        request_message: str = "REQUEST_WIFI",
        ping_interval_s: int = 5,
        ping_miss_limit: int = 12,
        connect_timeout_s: int = 60,
        creds_timeout_s: int = 60,
    ):
        if bluetooth is None:
            raise RuntimeError("bluetooth module is not available.")
        if aioble is None:
            raise RuntimeError("aioble is not available.")
        if asyncio is None:
            raise RuntimeError("uasyncio is not available.")

        self._device_name = device_name
        self._request_message = request_message
        self._ping_interval_s = ping_interval_s
        self._ping_miss_limit = ping_miss_limit
        self._connect_timeout_s = connect_timeout_s
        self._creds_timeout_s = creds_timeout_s
        print("[ble_provision] init device_name=%s" % device_name)

        self._ble = bluetooth.BLE()
        try:
            self._ble.active(True)
        except Exception:
            pass

        self._service = aioble.Service(_UART_SERVICE_UUID)
        self._rx_char = aioble.Characteristic(
            self._service, _UART_RX_UUID, write=True, capture=True
        )
        self._tx_char = aioble.Characteristic(
            self._service, _UART_TX_UUID, notify=True
        )
        aioble.register_services(self._service)
        self._receiver = BleCredentialReceiver()
        self._rx_buffer = b""

    async def _run(self) -> dict:
        print(
            "[ble_provision] waiting for credentials (connect=%ss creds=%ss)"
            % (self._connect_timeout_s, self._creds_timeout_s)
        )
        while True:
            connect_deadline = time.ticks_add(
                time.ticks_ms(), self._connect_timeout_s * 1000
            )
            print("[ble_provision] advertising name=%s" % self._device_name)
            try:
                async with await aioble.advertise(
                    100_000,
                    name=self._device_name,
                    services=[_UART_SERVICE_UUID],
                ) as connection:
                    result = await self._handle_connection(connection)
                    if result:
                        return result
            except Exception as exc:
                print("[ble_provision] advertise error: %s" % exc)
                await asyncio.sleep_ms(500)
                continue

            if time.ticks_diff(connect_deadline, time.ticks_ms()) <= 0:
                raise TimeoutError("BLE connection timed out.")

            print("[ble_provision] disconnected, re-advertising")

    async def _handle_connection(self, connection):
        print("[ble_provision] connected")
        self._save_connection_info(connection)
        self._receiver.reset()
        state = self._init_session_state()
        creds_deadline = time.ticks_add(
            time.ticks_ms(), self._creds_timeout_s * 1000
        )
        while time.ticks_diff(creds_deadline, time.ticks_ms()) > 0:
            data = await self._read_chunk(connection, state, creds_deadline)
            if data is None:
                if state.get("disconnect"):
                    break
                self._maybe_collect()
                continue
            if self._handle_payload(connection, state, data):
                self._maybe_collect()
                return state["config"]
            self._maybe_collect()
        print("[ble_provision] credentials timeout, reconnecting")
        self._receiver.reset()
        self._maybe_collect()
        return None

    def _init_session_state(self):
        return {
            "requested": False,
            "last_request": time.ticks_ms(),
            "connect_time": time.ticks_ms(),
            "missed": 0,
            "ping_enabled": True,
            "last_ping": time.ticks_ms(),
            "config": None,
            "disconnect": False,
        }

    async def _read_chunk(self, connection, state, creds_deadline):
        remaining_ms = time.ticks_diff(creds_deadline, time.ticks_ms())
        remaining_s = max(1, int(remaining_ms / 1000))
        wait_s = remaining_s
        if self._ping_interval_s:
            wait_s = min(wait_s, self._ping_interval_s)
        try:
            data = await asyncio.wait_for(self._rx_char.written(), wait_s)
        except asyncio.TimeoutError:
            data = None
        if not state["requested"] and self._request_message:
            self._maybe_send_request(connection, state)
        if data is None:
            self._maybe_ping(connection, state)
            return None
        if not data:
            return None
        print("[ble_provision] data: %r" % (data,))
        return data

    def _maybe_send_request(self, connection, state):
        if time.ticks_diff(time.ticks_ms(), state["connect_time"]) < 2000:
            return
        if time.ticks_diff(time.ticks_ms(), state["last_request"]) < 2000:
            return
        try:
            self._tx_char.notify(connection, self._request_message.encode())
        except Exception:
            pass
        else:
            print("[ble_provision] request sent")
        state["last_request"] = time.ticks_ms()

    def _maybe_ping(self, connection, state):
        if not state["ping_enabled"]:
            return
        if not self._ping_interval_s:
            return
        if time.ticks_diff(time.ticks_ms(), state["last_ping"]) < self._ping_interval_s * 1000:
            return
        try:
            self._tx_char.notify(connection, b"PING")
            print("[ble_provision] ping")
        except Exception as exc:
            print("[ble_provision] ping failed: %s" % exc)
        state["last_ping"] = time.ticks_ms()
        state["missed"] += 1
        if state["missed"] >= self._ping_miss_limit:
            print("[ble_provision] ping timeout, reconnecting")
            state["disconnect"] = True

    def _handle_payload(self, connection, state, data):
        payload = self._receiver.feed(data)
        if payload:
            if payload.get("type") == "credentials":
                print("[ble_provision] credentials received : %s" % (payload,))
                config = {
                    "ssid": payload.get("ssid", ""),
                    "password": payload.get("password", ""),
                    "session_code": payload.get("session_code", ""),
                }
                save_config(config)
                state["config"] = config
                try:
                    self._tx_char.notify(connection, b'{"type":"ack","status":"credentials_received"}\n')
                except Exception:
                    pass
                return True

            if payload.get("type") == "pong":
                state["missed"] = 0
                state["ping_enabled"] = False
                return False

            if payload.get("type") == "ping":
                try:
                    self._tx_char.notify(connection, b'{"type":"pong"}\n')
                except Exception:
                    pass

        if not isinstance(data, (bytes, bytearray, memoryview, str, tuple)):
            print("[ble_provision] unexpected payload type: %s" % type(data))

        state["requested"] = True
        return False

    def _maybe_collect(self):
        if not gc:
            return
        try:
            gc.collect()
        except Exception:
            pass

    def _save_connection_info(self, connection):
        info = {"device_name": self._device_name}
        try:
            info["connected_at_ms"] = time.ticks_ms()
        except Exception:
            pass
        try:
            dev = getattr(connection, "device", None)
            if dev is not None:
                addr = getattr(dev, "addr", None)
                if addr is not None:
                    info["peer_addr"] = str(addr)
                addr_type = getattr(dev, "addr_type", None)
                if addr_type is not None:
                    info["peer_addr_type"] = int(addr_type)
        except Exception:
            pass
        save_ble_info(info)

    def start(self):
        print("[ble_provision] start")

    def stop(self):
        print("[ble_provision] stop")
        self._shutdown_ble()

    def wait_for_credentials(self) -> dict:
        if asyncio is None:
            raise RuntimeError("uasyncio is not available.")
        return asyncio.run(self._run())

    def _shutdown_ble(self):
        if not self._ble:
            return
        try:
            self._ble.active(False)
        except Exception:
            pass
        self._maybe_collect()
        try:
            time.sleep_ms(100)
        except Exception:
            pass


def provision_via_ble(
    device_name: str = "BOMB-SETUP",
    timeout_s: int = 120,
    request_message: str = "REQUEST_WIFI",
) -> dict:
    print("[provision_via_ble] device_name=%s timeout=%s" % (device_name, timeout_s))
    provisioner = BleProvisioner(
        device_name=device_name,
        request_message=request_message,
        connect_timeout_s=timeout_s,
        creds_timeout_s=timeout_s,
    )
    provisioner.start()
    try:
        return provisioner.wait_for_credentials()
    finally:
        provisioner.stop()
        try:
            provisioner._shutdown_ble()
        except Exception:
            pass
        if gc:
            try:
                gc.collect()
            except Exception:
                pass
