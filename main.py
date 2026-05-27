try:
    import gc
except ImportError:
    gc = None

try:
    from bomb_device.config_store import load_config
except ImportError:
    from config_store import load_config


class GameDefinition:
    __slots__ = ("key", "name", "description", "runner")
    def __init__(self, key, name, description, runner):
        self.key = key
        self.name = name
        self.description = description
        self.runner = runner


class ActionDefinition:
    __slots__ = ("key", "name", "description", "runner")
    def __init__(self, key, name, description, runner):
        self.key = key
        self.name = name
        self.description = description
        self.runner = runner


def run_braille_game() -> None:
    """Import and run the Braille module."""
    from modules.braille.main import main as braille_main

    braille_main()


def run_simon_game() -> None:
    """Import and run the Simon module."""
    from modules.simon.simon import run_game as simon_main

    simon_main()


def run_suite_numerique_game() -> None:
    """Import and run the Suite Numerique module."""
    from modules.suite_numerique.main import main as suite_numerique_main

    suite_numerique_main()


def run_main_controller_loop(isDebug: bool = False) -> None:
    """Start the main ESP32 controller loop."""
    try:
        config = load_config() or {}
    except Exception as exc:
        print("Config load failed: %s" % exc)
        config = {}

    heartbeat_s = config.get("heartbeat_s", 5)
    broadcast_interval_ms = config.get("broadcast_interval_ms", 200)
    loop_delay_ms = config.get("loop_delay_ms", 50)

    if isDebug:
        from bomb_device.main_controller import MainController, DebugStateProvider

        print("Demarrage du controleur principal. Ctrl+C pour quitter.")
        controller = MainController(
            state_provider=DebugStateProvider(),
            heartbeat_s=heartbeat_s,
            broadcast_interval_ms=broadcast_interval_ms,
            loop_delay_ms=loop_delay_ms,
        )
        controller.run()
    else: 
        from bomb_device.main_controller import MainController
        from bomb_device.tcp_state_provider import TcpStateProvider

        host = config.get("tcp_host", "")
        port = config.get("tcp_port", 3200)
        session_code = config.get("session_code", "")
        if not session_code:
            print("Session code missing in config.json.")
            return
        if not host:
            print("TCP host missing in config.json.")
            return

        provider = TcpStateProvider(
            host,
            port,
            session_code,
            poll_interval_ms=config.get("tcp_poll_interval_ms", 500),
            connect_retry_ms=config.get("tcp_connect_retry_ms", 5000),
            timeout_s=config.get("tcp_timeout_s", 5),
            debug=config.get("tcp_debug", True),
            trace=config.get("tcp_trace", False),
            state_log_interval_ms=config.get("tcp_state_log_interval_ms", 5000),
        )
        controller = MainController(
            state_provider=provider,
            heartbeat_s=heartbeat_s,
            broadcast_interval_ms=broadcast_interval_ms,
            loop_delay_ms=loop_delay_ms,
        )
        controller.run()



def run_main_controller_pairing() -> None:
    """Run ESP-NOW pairing mode for the main controller."""
    from bomb_device.main_controller import MainController
    try:
        from bomb_device.provisioning import provision
    except ImportError:
        from provisioning import provision

    print("Provisioning (BLE preferred, fallback HTTP)...")
    try:
        provision(mode="ble", timeout_s=120)
        print("Provisioning complete.")
    except Exception as exc:
        print("Provisioning skipped/failed: %s" % exc)
        if gc:
            try:
                gc.collect()
            except Exception:
                pass
        return
    if gc:
        try:
            gc.collect()
        except Exception:
            pass

    controller = MainController()
    print("Mode appairage ESP-NOW actif (30 secondes).")
    controller.enter_pairing_mode(duration_s=30)
    print("Appairage termine.")


def show_device_info() -> None:
    try:
        config = load_config() or {}
    except Exception as exc:
        print("Config load failed: %s" % exc)
        config = {}

    print("Infos appareil:")
    print("1. Config")
    print("2. BLE status")
    print("3. WiFi status")
    print("4. Etat du jeu (via TCP poll)")
    choice = input("Votre choix: ").strip().lower()

    if choice == "1":
        print("Config:")
        for key in sorted(config.keys()):
            print("  %s: %s" % (key, config.get(key)))
        input("\nAppuyez sur Entree pour revenir au menu...")
        return

    if choice == "2":
        print("BLE status:")
        try:
            import bluetooth  # type: ignore
            print("  bluetooth: available")
        except Exception:
            print("  bluetooth: not available")
        try:
            import aioble  # type: ignore
            print("  aioble: available")
        except Exception:
            print("  aioble: not available")
        print("  note: connection status not tracked in runtime yet.")
        input("\nAppuyez sur Entree pour revenir au menu...")
        return

    if choice == "3":
        print("WiFi status:")
        try:
            import network  # type: ignore

            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            print("  connected: %s" % wlan.isconnected())
            try:
                print("  ssid: %s" % wlan.config("ssid"))
            except Exception:
                pass
            try:
                print("  ifconfig: %s" % (wlan.ifconfig(),))
            except Exception:
                pass
        except Exception as exc:
            print("  wifi error: %s" % exc)
        input("\nAppuyez sur Entree pour revenir au menu...")
        return

    if choice == "4":
        print("Etat du jeu:")
        from bomb_device.tcp_state_provider import TcpStateProvider

        host = config.get("tcp_host", "")
        port = config.get("tcp_port", 3200)
        session_code = config.get("session_code", "")
        if not session_code:
            print("  session_code manquant dans config.json")
            input("\nAppuyez sur Entree pour revenir au menu...")
            return
        if not host:
            print("  tcp_host manquant dans config.json")
            input("\nAppuyez sur Entree pour revenir au menu...")
            return

        provider = TcpStateProvider(
            host,
            port,
            session_code,
            poll_interval_ms=config.get("tcp_poll_interval_ms", 500),
            connect_retry_ms=config.get("tcp_connect_retry_ms", 5000),
            timeout_s=config.get("tcp_timeout_s", 5),
            debug=config.get("tcp_debug", True),
            trace=config.get("tcp_trace", False),
            state_log_interval_ms=config.get("tcp_state_log_interval_ms", 5000),
        )
        try:
            provider.connect(config)
            state = provider.poll_state() or {}
            if state:
                print("  %s" % state)
            else:
                print("  Aucun etat recu.")
        except Exception as exc:
            print("  Erreur: %s" % exc)
        input("\nAppuyez sur Entree pour revenir au menu...")
        return

    print("Choix invalide.")
    input("Appuyez sur Entree pour reessayer...")
GAMES = [
    GameDefinition("1", "Module Braille", "Decodez les sequences Braille pour desamorcer.", run_braille_game),
    GameDefinition("2", "Jeu Simon", "Appliquez la regle dependante du numero de serie.", run_simon_game),
    GameDefinition("3", "Suite Numerique", "Resoudre la suite numerique du module.", run_suite_numerique_game),
]

CONTROLLER_ACTIONS = [
    ActionDefinition(
        key="c",
        name="Controleur principal",
        description="Boucle principale ESP32 (etat + ESP-NOW).",
        runner=run_main_controller_loop,
    ),
    ActionDefinition(
        key="p",
        name="Appairage ESP-NOW",
        description="Detecte les secondaires et sauvegarde pairing.json.",
        runner=run_main_controller_pairing,
    ),
    ActionDefinition(
        key="i",
        name="Infos appareil",
        description="Afficher config, BLE/WiFi status, ou etat de jeu.",
        runner=show_device_info,
    ),
]


def clear_screen() -> None:
    # ANSI clear for serial terminals; harmless if unsupported.
    print("\x1b[2J\x1b[H", end="")


def show_menu() -> None:
    print("=" * 60)
    print("LEAVING BOX - LANCEUR DE MINI-JEUX")
    print("=" * 60)
    for game in GAMES:
        print(f"{game.key}. {game.name} - {game.description}")
    print("\nActions controleur principal:")
    for action in CONTROLLER_ACTIONS:
        print(f"{action.key}. {action.name} - {action.description}")
    print("a. Lancer tous les jeux consecutivement")
    print("q. Quitter")
    print("=" * 60)


def find_game(choice):
    for game in GAMES:
        if game.key == choice:
            return game
    return None


def find_action(choice):
    for action in CONTROLLER_ACTIONS:
        if action.key == choice:
            return action
    return None


def launch_game(game: GameDefinition) -> None:
    clear_screen()
    print(f"Lancement de {game.name}...")
    try:
        game.runner()
    except KeyboardInterrupt:
        print("\nJeu interrompu.")
    except Exception as exc:
        print(f"\nUne erreur est survenue: {exc}")
    finally:
        input("\nAppuyez sur Entree pour revenir au menu...")


def launch_action(action: ActionDefinition) -> None:
    clear_screen()
    print(f"Lancement: {action.name}...")
    try:
        action.runner()
    except KeyboardInterrupt:
        print("\nAction interrompue.")
    except Exception as exc:
        print(f"\nUne erreur est survenue: {exc}")
    finally:
        input("\nAppuyez sur Entree pour revenir au menu...")


def main() -> None:
    while True:
        clear_screen()
        show_menu()
        choice = input("Votre choix: ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            print("Fermeture du lanceur. A bientot !")
            break

        if choice == "a":
            for game in GAMES:
                launch_game(game)
            continue

        selected_game = find_game(choice)
        if selected_game:
            launch_game(selected_game)
            continue

        selected_action = find_action(choice)
        if selected_action:
            launch_action(selected_action)
            continue

        print("Choix invalide.")
        input("Appuyez sur Entree pour reessayer...")


if __name__ == "__main__":
    main()
