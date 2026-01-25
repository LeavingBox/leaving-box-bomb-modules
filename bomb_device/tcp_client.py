try:
    import ujson as json
except ImportError:
    import json

try:
    import usocket as socket
except ImportError:
    import socket


class DeviceTcpClient:
    def __init__(self, host, port, session_code, timeout_s=5, debug=True, trace=False):
        self.host = host
        self.port = int(port)
        self.session_code = session_code
        self.timeout_s = timeout_s
        self._sock = None
        self._debug = debug
        self._trace = trace

    def _log(self, message):
        if self._debug:
            print("[tcp_client]", message)

    def _resolve(self):
        return socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM)[0][-1]

    def connect(self):
        try:
            self._log("Connecting to %s:%s" % (self.host, self.port))
            addr = self._resolve()
            sock = socket.socket()
            sock.settimeout(self.timeout_s)
            sock.connect(addr)
            self._sock = sock
            self.send_json({"type": "hello", "sessionCode": self.session_code})
            response = self.recv_json(self.timeout_s)
            self._log("Hello response: %s" % response)
            return response
        except Exception as exc:
            self._sock = None
            self._log("Connect failed: %s" % (exc,))
            raise

    def send_json(self, payload):
        if not self._sock:
            self._log("Send skipped (no socket): %s" % payload)
            return
        data = json.dumps(payload) + "\n"
        if self._trace:
            self._log("Send: %s" % payload)
        self._sock.write(data)

    def recv_json(self, timeout_s=0):
        if not self._sock:
            return None
        try:
            if timeout_s:
                self._sock.settimeout(timeout_s)
            else:
                self._sock.settimeout(0)
            raw = self._sock.readline()
        except OSError:
            return None
        finally:
            if timeout_s:
                self._sock.settimeout(self.timeout_s)
        if not raw:
            return None
        try:
            message = json.loads(raw)
            if self._trace:
                self._log("Recv: %s" % message)
            return message
        except ValueError:
            self._log("Recv invalid JSON: %s" % raw)
            return None

    def close(self):
        if self._sock:
            self._sock.close()
            self._sock = None
            self._log("Closed connection.")

    def is_connected(self):
        return self._sock is not None
