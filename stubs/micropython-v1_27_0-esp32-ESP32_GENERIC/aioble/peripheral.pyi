"""
Module: 'aioble.peripheral' on micropython-v1.27.0-esp32-ESP32_GENERIC
"""
# MCU: {'variant': '', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC', 'mpy': 'v6.3', 'ver': '1.27.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.27.0'}
# Stubber: v1.26.5a0
from __future__ import annotations
from typing import Any, Final, Generator, AsyncGenerator
from _typeshed import Incomplete

def _peripheral_irq(*args, **kwargs) -> Incomplete:
    ...

def log_info(*args, **kwargs) -> Incomplete:
    ...

def log_warn(*args, **kwargs) -> Incomplete:
    ...

def log_error(*args, **kwargs) -> Incomplete:
    ...

def ensure_active(*args, **kwargs) -> Incomplete:
    ...

def _peripheral_shutdown(*args, **kwargs) -> Incomplete:
    ...

def const(*args, **kwargs) -> Incomplete:
    ...

def register_irq_handler(*args, **kwargs) -> Incomplete:
    ...

def _append(*args, **kwargs) -> Incomplete:
    ...

_connect_event: Incomplete ## <class 'NoneType'> = None

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

_incoming_connection: Incomplete ## <class 'NoneType'> = None

class DeviceTimeout():
    def _timeout_sleep(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...

ble: Incomplete ## <class 'BLE'> = <BLE>

class Device():
    def addr_hex(self, *args, **kwargs) -> Incomplete:
        ...

    def connect(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...

def advertise(*args, **kwargs) -> Generator:  ## = <generator>
    ...

