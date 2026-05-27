"""
Module: 'aioble.core' on micropython-v1.27.0-esp32-ESP32_GENERIC
"""
# MCU: {'variant': '', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC', 'mpy': 'v6.3', 'ver': '1.27.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.27.0'}
# Stubber: v1.26.5a0
from __future__ import annotations
from typing import Any, Final, Generator, AsyncGenerator
from _typeshed import Incomplete

log_level: int = 1
_shutdown_handlers: list = []
_irq_handlers: list = []
def ensure_active(*args, **kwargs) -> Incomplete:
    ...

def register_irq_handler(*args, **kwargs) -> Incomplete:
    ...

def config(*args, **kwargs) -> Incomplete:
    ...

def ble_irq(*args, **kwargs) -> Incomplete:
    ...

def stop(*args, **kwargs) -> Incomplete:
    ...

def log_error(*args, **kwargs) -> Incomplete:
    ...

def log_warn(*args, **kwargs) -> Incomplete:
    ...

def log_info(*args, **kwargs) -> Incomplete:
    ...

ble: Incomplete ## <class 'BLE'> = <BLE>

class GattError(Exception):
    ...
