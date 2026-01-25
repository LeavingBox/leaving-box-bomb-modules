try:
    import ujson as json
except ImportError:
    import json

import socket
import time

try:
    import network
except ImportError:
    network = None

try:
    from .config_store import save_config
except ImportError:
    from config_store import save_config

DEFAULT_AP_SSID = "BOMB-SETUP"
DEFAULT_PORT = 8080


def start_access_point(ap_ssid: str = DEFAULT_AP_SSID, ap_password: str = ""):
    if network is None:
        raise RuntimeError("network module is not available.")

    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    if ap_password:
        wlan.config(
            essid=ap_ssid,
            password=ap_password,
            authmode=network.AUTH_WPA_WPA2_PSK,
        )
    else:
        wlan.config(essid=ap_ssid)
    return wlan


def _read_request(conn, timeout_s: int):
    conn.settimeout(timeout_s)
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(512)
        if not chunk:
            break
        data += chunk
        if len(data) > 8192:
            break

    header_end = data.find(b"\r\n\r\n")
    if header_end == -1:
        return None

    header_bytes = data[:header_end]
    body = data[header_end + 4 :]

    try:
        header_text = header_bytes.decode()
    except UnicodeError:
        return None

    lines = header_text.split("\r\n")
    if not lines:
        return None

    try:
        method, path, _ = lines[0].split(" ", 2)
    except ValueError:
        return None

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

    content_length = int(headers.get("content-length", "0"))
    while len(body) < content_length:
        chunk = conn.recv(512)
        if not chunk:
            break
        body += chunk

    return method, path, headers, body


def _send_response(conn, status_code: int, body: str, content_type: str = "application/json"):
    status_text = "OK" if status_code == 200 else "ERROR"
    payload = body.encode()
    response = (
        "HTTP/1.1 %d %s\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n"
        % (status_code, status_text, content_type, len(payload))
    ).encode() + payload
    conn.sendall(response)


def serve_once(
    port: int = DEFAULT_PORT,
    timeout_s: int = 120,
    request_timeout_s: int = 5,
) -> dict:
    addr = ("0.0.0.0", port)
    listener = socket.socket()
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(addr)
    listener.listen(1)
    listener.settimeout(1)

    deadline = time.ticks_add(time.ticks_ms(), timeout_s * 1000)
    while time.ticks_diff(deadline, time.ticks_ms()) > 0:
        try:
            conn, _ = listener.accept()
        except OSError:
            continue

        try:
            request = _read_request(conn, request_timeout_s)
            if not request:
                _send_response(conn, 400, json.dumps({"error": "Bad request"}))
                continue

            method, path, _, body = request
            if method != "POST" or path != "/provision":
                _send_response(conn, 404, json.dumps({"error": "Not found"}))
                continue

            try:
                payload = json.loads(body.decode().strip() or "{}")
            except ValueError:
                _send_response(conn, 400, json.dumps({"error": "Invalid JSON"}))
                continue

            try:
                save_config(payload)
            except ValueError as exc:
                _send_response(conn, 400, json.dumps({"error": str(exc)}))
                continue

            _send_response(conn, 200, json.dumps({"status": "ok"}))
            return payload
        finally:
            try:
                conn.close()
            except OSError:
                pass

    raise TimeoutError("Provisioning timed out.")


def provision_via_http(
    ap_ssid: str = DEFAULT_AP_SSID,
    ap_password: str = "",
    port: int = DEFAULT_PORT,
    timeout_s: int = 120,
) -> dict:
    start_access_point(ap_ssid=ap_ssid, ap_password=ap_password)
    return serve_once(port=port, timeout_s=timeout_s)
