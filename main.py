import os
from dataclasses import dataclass
from typing import Callable, List, Optional

GameRunner = Callable[[], None]
ActionRunner = Callable[[], None]


@dataclass
class GameDefinition:
    key: str
    name: str
    description: str
    runner: GameRunner


@dataclass
class ActionDefinition:
    key: str
    name: str
    description: str
    runner: ActionRunner


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


def run_main_controller_loop() -> None:
    """Start the main ESP32 controller loop."""
    from esp32.main_controller import MainController

    print("Demarrage du controleur principal. Ctrl+C pour quitter.")
    controller = MainController()
    controller.run()


def run_main_controller_pairing() -> None:
    """Run ESP-NOW pairing mode for the main controller."""
    from esp32.main_controller import MainController

    controller = MainController()
    print("Mode appairage ESP-NOW actif (30 secondes).")
    controller.enter_pairing_mode(duration_s=30)
    print("Appairage termine.")


GAMES: List[GameDefinition] = [
    GameDefinition(
        key="1",
        name="Module Braille",
        description="Decodez les sequences Braille pour desamorcer.",
        runner=run_braille_game,
    ),
    GameDefinition(
        key="2",
        name="Jeu Simon",
        description="Appliquez la regle dependante du numero de serie.",
        runner=run_simon_game,
    ),
]

CONTROLLER_ACTIONS: List[ActionDefinition] = [
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
]


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


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


def find_game(choice: str) -> Optional[GameDefinition]:
    for game in GAMES:
        if game.key == choice:
            return game
    return None


def find_action(choice: str) -> Optional[ActionDefinition]:
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
