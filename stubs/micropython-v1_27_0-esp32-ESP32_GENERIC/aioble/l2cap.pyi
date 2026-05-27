"""
Module: 'aioble.l2cap' on micropython-v1.27.0-esp32-ESP32_GENERIC
"""
# MCU: {'variant': '', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC', 'mpy': 'v6.3', 'ver': '1.27.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.27.0'}
# Stubber: v1.26.5a0
from __future__ import annotations
from typing import Any, Final, Generator, AsyncGenerator
from _typeshed import Incomplete

_listening: bool = False
def const(*args, **kwargs) -> Incomplete:
    ...

def register_irq_handler(*args, **kwargs) -> Incomplete:
    ...

def _l2cap_irq(*args, **kwargs) -> Incomplete:
    ...

def _l2cap_shutdown(*args, **kwargs) -> Incomplete:
    ...

def log_error(*args, **kwargs) -> Incomplete:
    ...

ble: Incomplete ## <class 'BLE'> = <BLE>

class L2CAPChannel():
    def available(self, *args, **kwargs) -> Incomplete:
        ...

    def _assert_connected(self, *args, **kwargs) -> Incomplete:
        ...

    def disconnected(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def send(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def disconnect(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def recvinto(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def flush(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...

def connect(*args, **kwargs) -> Generator:  ## = <generator>
    ...

def accept(*args, **kwargs) -> Generator:  ## = <generator>
    ...


class L2CAPConnectionError(Exception):
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


class L2CAPDisconnectedError(Exception):
    ...
