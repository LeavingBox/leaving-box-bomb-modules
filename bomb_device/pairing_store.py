try:
    import ujson as json
except ImportError:
    import json

try:
    import ubinascii as binascii
except ImportError:
    import binascii

PAIRING_PATH = "pairing.json"


def mac_to_str(mac: bytes) -> str:
    return ":".join("{:02x}".format(b) for b in mac)


def str_to_mac(text: str) -> bytes:
    cleaned = text.replace(":", "").lower()
    return binascii.unhexlify(cleaned)


def load_pairing() -> dict:
    try:
        with open(PAIRING_PATH, "r") as handle:
            return json.loads(handle.read())
    except OSError:
        return {"version": 1, "next_game_id": 0, "peers": []}


def save_pairing(data: dict) -> None:
    with open(PAIRING_PATH, "w") as handle:
        handle.write(json.dumps(data))


def clear_pairing() -> None:
    try:
        import uos as os
    except ImportError:
        import os

    try:
        os.remove(PAIRING_PATH)
    except OSError:
        pass


def list_peers(data: dict) -> list:
    return data.get("peers", [])


def get_game_id_for_mac(data: dict, mac: bytes):
    mac_str = mac_to_str(mac)
    for entry in data.get("peers", []):
        if entry.get("mac") == mac_str:
            return entry.get("game_id")
    return None


def get_mac_for_game_id(data: dict, game_id: int):
    for entry in data.get("peers", []):
        if entry.get("game_id") == game_id:
            return str_to_mac(entry.get("mac"))
    return None


def assign_peer(data: dict, mac: bytes, game_type: str) -> int:
    existing = get_game_id_for_mac(data, mac)
    if existing is not None:
        return existing

    game_id = int(data.get("next_game_id", 0))
    data["next_game_id"] = game_id + 1

    entry = {
        "game_id": game_id,
        "mac": mac_to_str(mac),
        "game_type": (game_type or "").strip().lower(),
    }
    data.setdefault("peers", []).append(entry)
    return game_id
