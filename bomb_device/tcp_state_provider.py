import time

try:
    from .tcp_client import DeviceTcpClient
except ImportError:
    from tcp_client import DeviceTcpClient


class TcpStateProvider:
    def __init__(
        self,
        host,
        port,
        session_code,
        poll_interval_ms=500,
        connect_retry_ms=5000,
        timeout_s=5,
        debug=True,
        trace=False,
        state_log_interval_ms=5000,
    ):
        self.host = host
        self.port = int(port)
        self.session_code = session_code
        self.poll_interval_ms = poll_interval_ms
        self.connect_retry_ms = connect_retry_ms
        self.client = DeviceTcpClient(
            host, port, session_code, timeout_s=timeout_s, debug=debug, trace=trace
        )
        self._last_poll = 0
        self._last_poll_log = 0
        self._last_connect_attempt = 0
        self._last_state_log = 0
        self._cached_state = {}
        self._debug = debug
        self._state_log_interval_ms = state_log_interval_ms

    def _log(self, message):
        if self._debug:
            print("[tcp_state]", message)

    def connect(self, config):
        if config:
            host = config.get("tcp_host")
            port = config.get("tcp_port")
            poll_interval_ms = config.get("tcp_poll_interval_ms")
            connect_retry_ms = config.get("tcp_connect_retry_ms")
            state_log_interval_ms = config.get("tcp_state_log_interval_ms")
            timeout_s = config.get("tcp_timeout_s")
            debug = config.get("tcp_debug")
            trace = config.get("tcp_trace")

            if host:
                self.host = host
                self.client.host = host
            if port:
                self.port = int(port)
                self.client.port = int(port)
            if poll_interval_ms is not None:
                self.poll_interval_ms = int(poll_interval_ms)
            if connect_retry_ms is not None:
                self.connect_retry_ms = int(connect_retry_ms)
            if state_log_interval_ms is not None:
                self._state_log_interval_ms = int(state_log_interval_ms)
            if timeout_s is not None:
                self.client.timeout_s = int(timeout_s)
            if debug is not None:
                self._debug = bool(debug)
                self.client._debug = bool(debug)
            if trace is not None:
                self.client._trace = bool(trace)

        session_code = config.get("session_code") if config else None
        if session_code:
            self.session_code = session_code
            self.client.session_code = session_code
        self._log(
            "Connecting to %s:%s with session_code=%s"
            % (self.host, self.port, self.session_code)
        )
        try:
            response = self.client.connect()
            self._log("Connected: %s" % response)
        except Exception as exc:
            self._log("Connect failed: %s" % (exc,))

    def poll_state(self):
        now = time.ticks_ms()
        if not self.client.is_connected():
            if time.ticks_diff(now, self._last_connect_attempt) >= self.connect_retry_ms:
                self._log("Socket not connected, retrying connect...")
                self._last_connect_attempt = now
                self.connect({"session_code": self.session_code})
            return self._cached_state

        if time.ticks_diff(now, self._last_poll) >= self.poll_interval_ms:
            self.client.send_json(
                {"type": "poll", "sessionCode": self.session_code}
            )
            self._last_poll = now
            if time.ticks_diff(now, self._last_poll_log) >= 5000:
                self._log("Poll sent for %s" % self.session_code)
                self._last_poll_log = now

        message = self.client.recv_json(timeout_s=0)
        if not message:
            return self._cached_state

        if message.get("type") == "state":
            prev_state = self._cached_state
            new_state = {
                "barcode": message.get("barcode", ""),
                "ram": message.get("ram", 1),
                "time_left": message.get("timeLeft", 0),
                "strikes": message.get("strikes", 0),
                "started": bool(message.get("started", False)),
            }
            started_changed = prev_state.get("started") != new_state["started"]
            important_change = (
                prev_state.get("barcode") != new_state["barcode"]
                or prev_state.get("ram") != new_state["ram"]
                or prev_state.get("strikes") != new_state["strikes"]
                or started_changed
            )

            self._cached_state = new_state

            if started_changed:
                if new_state["started"]:
                    self._log("Game started.")
                else:
                    self._log("Game stopped.")

            now = time.ticks_ms()
            if important_change or time.ticks_diff(now, self._last_state_log) >= self._state_log_interval_ms:
                self._log("State updated: %s" % self._cached_state)
                self._last_state_log = now

        return self._cached_state

    def send_status(self, game_id, status, strikes):
        self._log("Status send: game_id=%s status=%s strikes=%s" % (game_id, status, strikes))
        self.client.send_json(
            {
                "type": "status",
                "sessionCode": self.session_code,
                "gameId": game_id,
                "status": status,
                "strikes": strikes,
            }
        )
