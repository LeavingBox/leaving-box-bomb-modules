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

        if isinstance(data, (bytes, bytearray)):
            if data == b"PONG":
                return {"type": "pong"}
            if data == b"PING":
                return {"type": "ping"}
        elif isinstance(data, str):
            if data == "PONG":
                return {"type": "pong"}
            if data == "PING":
                return {"type": "ping"}

        text = None
        if isinstance(data, (bytes, bytearray)):
            self._buffer += data
            if len(self._buffer) > self._max_buffer:
                self._buffer = self._buffer[-self._max_buffer :]
        elif isinstance(data, str):
            text = data

        if text is None and self._buffer:
            try:
                text = self._buffer.decode()
            except Exception:
                text = None

        if text:
            payload = self._try_parse_kv(text)
            if payload:
                payload["type"] = "credentials"
                return payload
            # Avoid re-processing the same chunks repeatedly.
            self._buffer = b""

        return None

    def _normalize(self, raw):
        if isinstance(raw, tuple):
            if len(raw) >= 2 and isinstance(raw[1], (bytes, bytearray, memoryview, str)):
                raw = raw[1]
            else:
                raw = raw[0]
        if isinstance(raw, memoryview):
            raw = bytes(raw)
        if isinstance(raw, (bytes, bytearray, str)):
            return raw
        return None

    def _try_parse_kv(self, text):
        text = text.replace("\n", ";").replace("&", ";")
        # Ensure key boundaries even if chunks were concatenated without ';'
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
                self._kv_state[key] = ""  # placeholder until complete
            else:
                self._kv_state[key] = value
        
        if self._is_complete(self._kv_state):
            password = "".join(self._password_parts)
            payload = {
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
