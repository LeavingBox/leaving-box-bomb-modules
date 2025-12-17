import os
from dataclasses import dataclass
from typing import Callable, List, Optional

GameRunner = Callable[[], None]


@dataclass
class GameDefinition:
    key: str
    name: str
    description: str
    runner: GameRunner


def run_braille_game() -> None:
    """Import and run the Braille module."""
    from modules.braille.main import main as braille_main

    braille_main()


def run_simon_game() -> None:
    """Import and run the Simon module."""
    from modules.simon.simon import run_game as simon_main

    simon_main()


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


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def show_menu() -> None:
    print("=" * 60)
    print("LEAVING BOX - LANCEUR DE MINI-JEUX")
    print("=" * 60)
    for game in GAMES:
        print(f"{game.key}. {game.name} - {game.description}")
    print("a. Lancer tous les jeux consecutivement")
    print("q. Quitter")
    print("=" * 60)


def find_game(choice: str) -> Optional[GameDefinition]:
    for game in GAMES:
        if game.key == choice:
            return game
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
        else:
            print("Choix invalide.")
            input("Appuyez sur Entree pour reessayer...")


if __name__ == "__main__":
    main()
