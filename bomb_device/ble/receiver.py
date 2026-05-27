import json


class BleCredentialReceiver:
    def __init__(self, max_buffer=2048, debug=True):
        self._max_buffer = max_buffer
        self._debug = debug
        self.reset()

    def _log(self, message):
        if self._debug:
            print(message)

    def reset(self):
        self._buffer = b""
        self._kv_state = {}
        self._password_parts = []

    def feed(self, raw):
        data = self._normalize(raw)
        if data is None:
            return None

        # Gestion immediate des messages simples
        simple = self._parse_simple_message(data)
        if simple:
            return simple

        # Convertir tout en bytes pour unifier le buffer
        if isinstance(data, str):
            data = data.encode("utf-8")

        self._buffer += data

        # Limiter la taille memoire
        if len(self._buffer) > self._max_buffer:
            self._buffer = self._buffer[-self._max_buffer:]

        self._log("[ble_provision] buffer=%r" % self._buffer)

        # 1) Priorite au framing par ligne: JSON ou texte termine par \n
        while b"\n" in self._buffer:
            raw_line, self._buffer = self._buffer.split(b"\n", 1)
            raw_line = raw_line.strip()

            if not raw_line:
                continue

            payload = self._parse_complete_message(raw_line)
            if payload:
                return payload

        # 2) Fallback legacy KV sans newline :
        # si on voit clairement les cles, on tente un parse progressif
        try:
            text = self._buffer.decode("utf-8")
        except Exception:
            return None

        if any(key in text for key in ("ssid=", "password=", "session_code=")):
            payload = self._try_parse_kv(text)
            if payload:
                # le message legacy a ete consomme
                self._buffer = b""
                return payload

        return None

    def _normalize(self, raw):
        if isinstance(raw, tuple):
            if len(raw) >= 2 and isinstance(raw[1], (bytes, bytearray, memoryview, str)):
                raw = raw[1]
            else:
                raw = raw[0]

        if isinstance(raw, memoryview):
            raw = bytes(raw)

        if isinstance(raw, bytearray):
            raw = bytes(raw)

        if isinstance(raw, (bytes, str)):
            return raw

        return None

    def _parse_simple_message(self, data):
        if isinstance(data, bytes):
            stripped = data.strip()
            if stripped == b"PONG":
                return {"type": "pong"}
            if stripped == b"PING":
                return {"type": "ping"}

        if isinstance(data, str):
            stripped = data.strip()
            if stripped == "PONG":
                return {"type": "pong"}
            if stripped == "PING":
                return {"type": "ping"}

        return None

    def _parse_complete_message(self, raw_line):
        self._log("[ble_provision] full message: %r" % raw_line)

        # Messages simples
        if raw_line == b"PONG":
            return {"type": "pong"}
        if raw_line == b"PING":
            return {"type": "ping"}

        # 1) Essai JSON
        try:
            text = raw_line.decode("utf-8")
            payload = json.loads(text)
            self._log("[ble_provision] parsed json payload: %s" % payload)

            if isinstance(payload, dict):
                if payload.get("type") == "credentials":
                    return {
                        "type": "credentials",
                        "ssid": payload.get("ssid", ""),
                        "password": payload.get("password", ""),
                        "session_code": payload.get("session_code", ""),
                    }
                if payload.get("type") == "ping":
                    return {"type": "ping"}
                if payload.get("type") == "pong":
                    return {"type": "pong"}
        except Exception as exc:
            self._log("[ble_provision] json parse failed: %s" % exc)

        # 2) Essai KV legacy
        try:
            text = raw_line.decode("utf-8")
        except Exception:
            return None

        payload = self._try_parse_kv(text)
        if payload:
            return payload

        return None

    def _try_parse_kv(self, text):
        text = text.replace("\n", ";").replace("&", ";")

        # Garantir les separations de cles
        for key in ("ssid=", "password=", "session_code="):
            text = text.replace(key, ";" + key)

        parts = text.split(";")
        self._log("[ble_provision] parsing kv parts: %s" % parts)

        for part in parts:
            part = part.strip()
            if not part or "=" not in part:
                continue

            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key == "password" and value:
                if self._password_parts and self._password_parts[-1] == value:
                    continue
                self._password_parts.append(value)
                self._kv_state[key] = ""
            else:
                self._kv_state[key] = value

        if self._is_complete(self._kv_state):
            password = "".join(self._password_parts)
            payload = {
                "type": "credentials",
                "ssid": self._kv_state.get("ssid", ""),
                "password": password,
                "session_code": self._kv_state.get("session_code", ""),
            }
            self.reset()
            return payload

        return None

    def _is_complete(self, payload):
        if not payload.get("ssid") or not payload.get("session_code"):
            return False
        if not self._password_parts:
            return False
        return True