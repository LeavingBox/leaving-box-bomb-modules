# ESP32 provisioning

This folder contains MicroPython helpers to provision Wi-Fi + session code using:
- HTTP POST from the mobile app (no web UI on the device).
- BLE UART (simple BLE write from the app).

## HTTP provisioning (app assisted)

1) Put the main controller in setup mode (hold the setup button).
2) The device opens the `BOMB-SETUP` Wi-Fi AP.
3) The mobile app sends a JSON payload to:

```
POST http://192.168.4.1:8080/provision
```

Payload example:

```json
{
  "ssid": "MyWifi",
  "password": "MyPassword",
  "session_code": "A1B2C3"
}
```

## BLE provisioning

1) Put the main controller in setup mode (hold the setup button).
2) The device advertises BLE name `BOMB-SETUP`.
3) The mobile app writes a line to the RX characteristic:

```
ssid=MyWifi;password=MyPassword;session_code=A1B2C3\n
```

## Files

- `config_store.py`: stores config in `config.json` on the device.
- `provision_http.py`: HTTP POST provisioning server.
- `provision_ble.py`: BLE UART provisioning.
- `provisioning.py`: wrappers to select the method.
- `protocol.py`: fixed-size ESP-NOW message format.
- `espnow_bus.py`: thin ESP-NOW wrapper.
- `pairing_store.py`: stores paired secondary controllers in `pairing.json`.
- `wifi_manager.py`: Wi-Fi connect helper.
- `main_controller.py`: main controller polling loop (ESP-NOW + API bridge).

## Usage notes

Copy these files to the device root or add `/bomb_device` to `sys.path` so imports work.

## Main controller loop

`main_controller.py` broadcasts the current game state to all paired secondary
controllers and receives their status updates. It expects a state provider that
polls the API (TCP or other).

You can start the loop on the device by renaming `main_controller.py` to
`main.py`, or importing and running `MainController`.

```python
from bomb_device.main_controller import MainController

controller = MainController()
controller.run()
```

## Pairing mode

When you want to pair secondary controllers:
1) Put the main controller in pairing mode (call `enter_pairing_mode()`).
2) Each secondary should send a `MSG_HELLO` frame with its game type.
3) The main controller saves the mapping into `pairing.json`.

Example:

```python
from bomb_device.main_controller import MainController

controller = MainController()
controller.enter_pairing_mode(duration_s=30)
```

The stored pairing survives reboot.

## TCP client (device -> API)

Use `tcp_client.py` and `tcp_state_provider.py` to connect to the API device TCP.
Example usage with the main controller:

```python
from bomb_device.main_controller import MainController
from bomb_device.tcp_state_provider import TcpStateProvider

provider = TcpStateProvider("host.docker.internal", 3200, "ABC123")
controller = MainController(state_provider=provider, heartbeat_s=5)
controller.run()
```
