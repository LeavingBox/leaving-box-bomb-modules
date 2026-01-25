try:
    import ustruct as struct
except ImportError:
    import struct

MSG_STATE = 0x01
MSG_STATUS = 0x02
MSG_HELLO = 0x10
MSG_PAIR_ACK = 0x11

BARCODE_LEN = 11
FRAME_LEN = 19


def _xor_checksum(payload: bytes) -> int:
    value = 0
    for byte in payload:
        value ^= byte
    return value & 0xFF


def _pad_barcode(barcode: str) -> bytes:
    text = (barcode or "").strip().upper()
    raw = text.encode()
    if len(raw) > BARCODE_LEN:
        raw = raw[:BARCODE_LEN]
    if len(raw) < BARCODE_LEN:
        raw = raw + (b"\x00" * (BARCODE_LEN - len(raw)))
    return raw


def _decode_barcode(raw: bytes) -> str:
    if not raw:
        return ""
    return raw.split(b"\x00", 1)[0].decode()


def pack_state(game_id: int, barcode: str, ram: int, strikes: int, time_left: int) -> bytes:
    barcode_bytes = _pad_barcode(barcode)
    payload = struct.pack(
        ">BBBBH",
        MSG_STATE,
        game_id & 0xFF,
        ram & 0xFF,
        strikes & 0xFF,
        time_left & 0xFFFF,
    ) + struct.pack(">B", 0) + barcode_bytes
    checksum = _xor_checksum(payload)
    return payload + struct.pack(">B", checksum)


def pack_status(game_id: int, status: int, strikes: int = 0, time_left: int = 0) -> bytes:
    barcode_bytes = b"\x00" * BARCODE_LEN
    payload = struct.pack(
        ">BBBBH",
        MSG_STATUS,
        game_id & 0xFF,
        0,
        strikes & 0xFF,
        time_left & 0xFFFF,
    ) + struct.pack(">B", status & 0xFF) + barcode_bytes
    checksum = _xor_checksum(payload)
    return payload + struct.pack(">B", checksum)


def pack_hello(game_type: str) -> bytes:
    barcode_bytes = _pad_barcode(game_type)
    payload = struct.pack(">BBBBH", MSG_HELLO, 0xFF, 0, 0, 0) + struct.pack(">B", 0) + barcode_bytes
    checksum = _xor_checksum(payload)
    return payload + struct.pack(">B", checksum)


def pack_pair_ack(game_id: int, game_type: str) -> bytes:
    barcode_bytes = _pad_barcode(game_type)
    payload = struct.pack(">BBBBH", MSG_PAIR_ACK, game_id & 0xFF, 0, 0, 0) + struct.pack(">B", 0) + barcode_bytes
    checksum = _xor_checksum(payload)
    return payload + struct.pack(">B", checksum)


def unpack(frame: bytes) -> dict:
    if not frame or len(frame) != FRAME_LEN:
        return {"valid": False, "error": "length"}

    payload = frame[:-1]
    checksum = frame[-1]
    if _xor_checksum(payload) != checksum:
        return {"valid": False, "error": "checksum"}

    msg_type, game_id, ram, strikes, time_left = struct.unpack(">BBBBH", payload[:6])
    status = payload[6]
    barcode = _decode_barcode(payload[7:])

    return {
        "valid": True,
        "msg_type": msg_type,
        "game_id": game_id,
        "ram": ram,
        "strikes": strikes,
        "time_left": time_left,
        "status": status,
        "barcode": barcode,
    }
