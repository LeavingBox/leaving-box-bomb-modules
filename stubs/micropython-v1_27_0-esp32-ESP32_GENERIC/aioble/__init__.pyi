"""
Module: 'aioble.__init__' on micropython-v1.27.0-esp32-ESP32_GENERIC
"""
# MCU: {'variant': '', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC', 'mpy': 'v6.3', 'ver': '1.27.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.27.0'}
# Stubber: v1.26.5a0
from __future__ import annotations
from typing import Any, Final, Generator, AsyncGenerator
from _typeshed import Incomplete

ADDR_RANDOM: Final[int] = 1
ADDR_PUBLIC: Final[int] = 0
def log_error(*args, **kwargs) -> Incomplete:
    ...

def log_warn(*args, **kwargs) -> Incomplete:
    ...

def stop(*args, **kwargs) -> Incomplete:
    ...

def register_services(*args, **kwargs) -> Incomplete:
    ...

def const(*args, **kwargs) -> Incomplete:
    ...

def log_info(*args, **kwargs) -> Incomplete:
    ...

def config(*args, **kwargs) -> Incomplete:
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


class scan():
    def cancel(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class DeviceDisconnectedError(Exception):
    ...

class Device():
    def addr_hex(self, *args, **kwargs) -> Incomplete:
        ...

    def connect(self, *args, **kwargs) -> Generator:  ## = <generator>
        ...

    def __init__(self, *argv, **kwargs) -> None:
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


class GattError(Exception):
    ...
def advertise(*args, **kwargs) -> Generator:  ## = <generator>
    ...


class Service():
    def _tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...

