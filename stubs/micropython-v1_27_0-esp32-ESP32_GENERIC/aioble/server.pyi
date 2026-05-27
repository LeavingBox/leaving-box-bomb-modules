"""
Module: 'aioble.server' on micropython-v1.27.0-esp32-ESP32_GENERIC
"""
# MCU: {'variant': '', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC', 'mpy': 'v6.3', 'ver': '1.27.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.27.0'}
# Stubber: v1.26.5a0
from __future__ import annotations
from typing import Any, Final, Generator, AsyncGenerator
from _typeshed import Incomplete

_registered_characteristics: dict = {}
def register_irq_handler(*args, **kwargs) -> Incomplete:
    ...

def const(*args, **kwargs) -> Incomplete:
    ...

def register_services(*args, **kwargs) -> Incomplete:
    ...

def _server_shutdown(*args, **kwargs) -> Incomplete:
    ...

def ensure_active(*args, **kwargs) -> Incomplete:
    ...

def _server_irq(*args, **kwargs) -> Incomplete:
    ...

def log_warn(*args, **kwargs) -> Incomplete:
    ...

def log_error(*args, **kwargs) -> Incomplete:
    ...

def log_info(*args, **kwargs) -> Incomplete:
    ...


class Characteristic():
    def _tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def _register(self, *args, **kwargs) -> Incomplete:
        ...

    def on_read(self, *args, **kwargs) -> Incomplete:
        ...

    def _init_capture(self, *args, **kwargs) -> Incomplete:
        ...

    def notify(self, *args, **kwargs) -> Incomplete:
        ...

    def write(self, *args, **kwargs) -> Incomplete:
        ...

    def read(self, *args, **kwargs) -> Incomplete:
        ...

    def _indicate_done(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_write(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_read(self, *args, **kwargs) -> Incomplete:
        ...

    def indicate(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def written(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def _run_capture_task(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class DeviceConnection():
    _connected: dict = {}
    def is_connected(self, *args, **kwargs) -> Incomplete:
        ...

    def _run_task(self, *args, **kwargs) -> Incomplete:
        ...

    def services(self, *args, **kwargs) -> Incomplete:
        ...

    def timeout(self, *args, **kwargs) -> Incomplete:
        ...

    def l2cap_accept(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def exchange_mtu(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def pair(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def l2cap_connect(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def service(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def disconnect(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def device_task(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def disconnected(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class BaseCharacteristic():
    def _register(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_read(self, *args, **kwargs) -> Incomplete:
        ...

    def _init_capture(self, *args, **kwargs) -> Incomplete:
        ...

    def on_read(self, *args, **kwargs) -> Incomplete:
        ...

    def read(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_write(self, *args, **kwargs) -> Incomplete:
        ...

    def write(self, *args, **kwargs) -> Incomplete:
        ...

    def _run_capture_task(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def written(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class deque():
    def pop(self, *args, **kwargs) -> Incomplete:
        ...

    def appendleft(self, *args, **kwargs) -> Incomplete:
        ...

    def popleft(self, *args, **kwargs) -> Incomplete:
        ...

    def extend(self, *args, **kwargs) -> Incomplete:
        ...

    def append(self, *args, **kwargs) -> Incomplete:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class Descriptor():
    def on_read(self, *args, **kwargs) -> Incomplete:
        ...

    def _register(self, *args, **kwargs) -> Incomplete:
        ...

    def _tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def _init_capture(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_read(self, *args, **kwargs) -> Incomplete:
        ...

    def read(self, *args, **kwargs) -> Incomplete:
        ...

    def write(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_write(self, *args, **kwargs) -> Incomplete:
        ...

    def _run_capture_task(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def written(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class DeviceTimeout():
    def _timeout_sleep(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class BufferedCharacteristic():
    def _indicate_done(self, *args, **kwargs) -> Incomplete:
        ...

    def notify(self, *args, **kwargs) -> Incomplete:
        ...

    def _tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def _init_capture(self, *args, **kwargs) -> Incomplete:
        ...

    def on_read(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_read(self, *args, **kwargs) -> Incomplete:
        ...

    def read(self, *args, **kwargs) -> Incomplete:
        ...

    def write(self, *args, **kwargs) -> Incomplete:
        ...

    def _remote_write(self, *args, **kwargs) -> Incomplete:
        ...

    def indicate(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def _register(self, *args, **kwargs) -> Incomplete:
        ...

    def written(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def _run_capture_task(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class GattError(Exception):
    ...

class Service():
    def _tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...

ble: Incomplete ## <class 'BLE'> = <BLE>
