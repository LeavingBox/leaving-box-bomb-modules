"""
Module: 'aioble.security' on micropython-v1.27.0-esp32-ESP32_GENERIC
"""
# MCU: {'variant': '', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC', 'mpy': 'v6.3', 'ver': '1.27.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.27.0'}
# Stubber: v1.26.5a0
from __future__ import annotations
from typing import Any, Final, Generator, AsyncGenerator
from _typeshed import Incomplete

_DEFAULT_PATH: Final[str] = 'ble_secrets.json'
_modified: bool = False
_secrets: dict = {}
def register_irq_handler(*args, **kwargs) -> Incomplete:
    ...

def _security_shutdown(*args, **kwargs) -> Incomplete:
    ...

def load_secrets(*args, **kwargs) -> Incomplete:
    ...

def _security_irq(*args, **kwargs) -> Incomplete:
    ...

def _save_secrets(*args, **kwargs) -> Incomplete:
    ...

def const(*args, **kwargs) -> Incomplete:
    ...

def schedule(*args, **kwargs) -> Incomplete:
    ...

def log_warn(*args, **kwargs) -> Incomplete:
    ...

def log_info(*args, **kwargs) -> Incomplete:
    ...

_path: Incomplete ## <class 'NoneType'> = None
def pair(*args, **kwargs) -> Generator:  ## = <generator>
    ...

ble: Incomplete ## <class 'BLE'> = <BLE>

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

