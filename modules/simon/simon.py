import random
from typing import Dict, List, Optional

COLORS: List[str] = ["Rouge", "Jaune", "Bleu", "Vert"]
DEFAULT_SERIAL = "HHG345DGJ"


def get_rule(serial: str) -> Dict[str, str]:
    """Return the color mapping rule that depends on the serial number."""
    if not serial:
        raise ValueError("Le numero de serie ne peut pas etre vide.")

    start_is_digit = serial[0].isdigit()
    end_is_digit = serial[-1].isdigit()

    if start_is_digit and not end_is_digit:
        return {"Bleu": "Jaune", "Jaune": "Rouge", "Vert": "Bleu", "Rouge": "Vert"}

    if start_is_digit and end_is_digit:
        return {"Rouge": "Jaune", "Jaune": "Bleu", "Bleu": "Vert", "Vert": "Rouge"}

    if not start_is_digit and not end_is_digit:
        return {"Rouge": "Bleu", "Bleu": "Rouge", "Jaune": "Vert", "Vert": "Jaune"}

    # start is not a digit and end is a digit
    return {color: color for color in COLORS}


def prompt_transformed_sequence(sequence: List[str], rule: Dict[str, str]) -> bool:
    """Ask the player for the transformed sequence and return True if it is correct."""
    print("Entrez la sequence transformee :")
    for color in sequence:
        converted = rule[color]
        answer = input(f"Pour {color} -> ").strip().capitalize()
        if answer != converted:
            return False
    return True


def run_game(serial: str = DEFAULT_SERIAL, rng: Optional[random.Random] = None) -> None:
    """Run the Simon game loop using the provided serial number."""
    rule = get_rule(serial)
    rng = rng or random.Random()
    sequence: List[str] = []
    score = 0

    print("Jeu Simon - Version Numero de Serie")
    print("Numero de serie :", serial)

    while True:
        sequence.append(rng.choice(COLORS))

        print("\nSequence :")
        for color in sequence:
            print(color)

        if not prompt_transformed_sequence(sequence, rule):
            print("Erreur ! Fin du jeu.")
            print("Score final :", score)
            break

        score += 1
        print("Correct ! Score :", score)


if __name__ == "__main__":
    run_game()
