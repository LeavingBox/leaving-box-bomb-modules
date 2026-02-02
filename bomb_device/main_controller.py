import time

try:
    from .config_store import (load_config, save_config)
    from .espnow_bus import EspNowBus
    from .protocol import (
        MSG_HELLO,
        MSG_STATUS,
        pack_pair_ack,
        pack_state,
        unpack,
    )
    from . import pairing_store
    from . import wifi_manager
except ImportError:
    from config_store import (load_config, save_config)
    from espnow_bus import EspNowBus
    from protocol import (
        MSG_HELLO,
        MSG_STATUS,
        pack_pair_ack,
        pack_state,
        unpack,
    )
    import pairing_store
    import wifi_manager


class GameState:
    def __init__(self):
        self.barcode = ""
        self.ram = 1
        self.time_left = 0
        self.strikes = 0
        self.started = False
        self.status_by_game = {}

    def apply_update(self, update: dict) -> None:
        if not update:
            return
        if "barcode" in update:
            self.barcode = update["barcode"]
        if "ram" in update:
            self.ram = int(update["ram"])
        if "time_left" in update:
            self.time_left = int(update["time_left"])
        if "strikes" in update:
            self.strikes = int(update["strikes"])
        if "started" in update:
            self.started = bool(update["started"])


class NullStateProvider:
    def connect(self, config: dict) -> None:
        return None

    def poll_state(self) -> dict:
        return {}

    def send_status(self, game_id: int, status: int, strikes: int) -> None:
        return None


class DebugStateProvider(NullStateProvider):
    def __init__(
        self,
        barcode="ED038HD92L6",
        ram=1,
        time_left=300,
        strikes=0,
        tick_ms=1000,
    ):
        self.barcode = barcode
        self.ram = ram
        self.time_left = time_left
        self.strikes = strikes
        self._tick_ms = tick_ms
        self._last_tick = time.ticks_ms()

    def poll_state(self) -> dict:
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_tick) < self._tick_ms:
            return {}

        self._last_tick = now
        if self.time_left > 0:
            self.time_left -= 1

        return {
            "barcode": self.barcode,
            "ram": self.ram,
            "time_left": self.time_left,
            "strikes": self.strikes,
        }


class MainController:
    def __init__(
        self,
        state_provider=None,
        broadcast_interval_ms=200,
        loop_delay_ms=50,
        bus=None,
        heartbeat_s=0,
    ):
        self.state_provider = state_provider or NullStateProvider()
        self.broadcast_interval_ms = broadcast_interval_ms
        self.loop_delay_ms = loop_delay_ms
        self.heartbeat_ms = int(heartbeat_s * 1000) if heartbeat_s else 0

        self.state = GameState()
        self.pairing = pairing_store.load_pairing()
        self.bus = bus or EspNowBus()
        self.bus.init()

        for entry in pairing_store.list_peers(self.pairing):
            mac = pairing_store.str_to_mac(entry["mac"])
            self.bus.add_peer(mac)

        print("Loading WiFi configuration...")
        config = load_config()
        if config and config.get("ssid"):
            try:
                print("Connecting to WiFi SSID: %s" % ( config.get("ssid", ""),))
                wifi_manager.connect_wifi(
                    config.get("ssid", ""),
                    config.get("password", ""),
                    config.get("wifi_timeout_s", 15),
                )
                print("WiFi connected.")
            except Exception as e:
                print("WiFi connection failed: %s" % e)
        else:
            print("No WiFi config found.")

        try:
            self.state_provider.connect(config or {})
            print("State provider connected.")
        except Exception as e:
            print("State provider connect failed: %s" % e)

    def enter_pairing_mode(self, duration_s=30):
        deadline = time.ticks_add(time.ticks_ms(), duration_s * 1000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            mac, msg = self.bus.recv(200)
            if not mac or not msg:
                continue
            data = unpack(msg)
            if not data.get("valid"):
                continue
            if data["msg_type"] != MSG_HELLO:
                continue

            game_type = data.get("barcode") or "game"
            game_id = pairing_store.assign_peer(self.pairing, mac, game_type)
            pairing_store.save_pairing(self.pairing)
            self.bus.add_peer(mac)
            ack = pack_pair_ack(game_id, game_type)
            self.bus.send(mac, ack, True)

    def _broadcast_state(self):
        for entry in pairing_store.list_peers(self.pairing):
            mac = pairing_store.str_to_mac(entry["mac"])
            payload = pack_state(
                entry["game_id"],
                self.state.barcode,
                self.state.ram,
                self.state.strikes,
                self.state.time_left,
            )
            self.bus.send(mac, payload, False)

    def _handle_incoming(self):
        while True:
            mac, msg = self.bus.recv(0)
            if not mac or not msg:
                break
            data = unpack(msg)
            if not data.get("valid"):
                continue

            if data["msg_type"] == MSG_STATUS:
                game_id = data["game_id"]
                self.state.status_by_game[game_id] = data["status"]
                self.state_provider.send_status(
                    game_id,
                    data["status"],
                    data["strikes"],
                )

    def run(self):
        last_broadcast = time.ticks_ms()
        last_heartbeat = time.ticks_ms()
        while True:
            update = self.state_provider.poll_state()
            if update:
                prev_started = self.state.started
                self.state.apply_update(update)
                if "started" in update and prev_started != self.state.started:
                    self._handle_started_transition(self.state.started)

            self._handle_incoming()

            if (
                time.ticks_diff(time.ticks_ms(), last_broadcast)
                >= self.broadcast_interval_ms
            ):
                self._broadcast_state()
                last_broadcast = time.ticks_ms()

            if self.heartbeat_ms:
                now = time.ticks_ms()
                if time.ticks_diff(now, last_heartbeat) >= self.heartbeat_ms:
                    peers = len(pairing_store.list_peers(self.pairing))
                    print(
                        "Heartbeat: time_left=%s strikes=%s peers=%s"
                        % (self.state.time_left, self.state.strikes, peers)
                    )
                    last_heartbeat = now

            time.sleep_ms(self.loop_delay_ms)

    def _handle_started_transition(self, started):
        if started:
            print("Session started.")
        else:
            print("Session stopped.")


if __name__ == "__main__":
    controller = MainController()
    controller.run()
