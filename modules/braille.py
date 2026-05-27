from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import time

# =========================
# Configuration hardware
# =========================

# Boutons braille
P1 = Pin(23, Pin.IN, Pin.PULL_UP)
P2 = Pin(18, Pin.IN, Pin.PULL_UP)
P3 = Pin(19, Pin.IN, Pin.PULL_UP)
P4 = Pin(21, Pin.IN, Pin.PULL_UP)
P5 = Pin(22, Pin.IN, Pin.PULL_UP)
P6 = Pin(4, Pin.IN, Pin.PULL_UP)
VALID = Pin(5, Pin.IN, Pin.PULL_UP)

# LEDs
LED_VERTE = Pin(2, Pin.OUT)
LED_ROUGE = Pin(15, Pin.OUT)

# OLED SSD1306 I2C
I2C_OLED = SoftI2C(scl=Pin(26), sda=Pin(27))
OLED = SSD1306_I2C(128, 64, I2C_OLED)

# =========================
# Variables globales
# =========================

SERIAL_CODE = "AB48320"   # Exemple de code de serie reel

mot_lettres = ["_", "_", "_", "_"]      # lettres finales attendues
mot_genere = [0, 0, 0, 0]               # valeurs braille attendues
mot_affiche = ["_", "_", "_", "_"]      # affichage OLED

lettre_actuelle = 0
etat_braille = [0, 0, 0, 0, 0, 0]

dernier_etat = [1, 1, 1, 1, 1, 1]
last_debounce_time = [0, 0, 0, 0, 0, 0]
debounce_delay = 50  # ms

special_a_tous_points = False


# =========================
# Tables Braille A-Z
# =========================

LETTER_TO_BRAILLE = {
    "A": 0b100000,
    "B": 0b110000,
    "C": 0b100100,
    "D": 0b100110,
    "E": 0b100010,
    "F": 0b110100,
    "G": 0b110110,
    "H": 0b110010,
    "I": 0b010100,
    "J": 0b010110,
    "K": 0b101000,
    "L": 0b111000,
    "M": 0b101100,
    "N": 0b101110,
    "O": 0b101010,
    "P": 0b111100,
    "Q": 0b111110,
    "R": 0b111010,
    "S": 0b011100,
    "T": 0b011110,
    "U": 0b101001,
    "V": 0b111001,
    "W": 0b010111,
    "X": 0b101101,
    "Y": 0b101111,
    "Z": 0b101011,
}

BRAILLE_TO_LETTER = {}
for k in LETTER_TO_BRAILLE:
    BRAILLE_TO_LETTER[LETTER_TO_BRAILLE[k]] = k

ALL_DOTS_ACTIVE = 0b111111


# =========================
# Utilitaires debug
# =========================

def afficher_etat():
    print("Etat Braille: [", end="")
    for i in range(6):
        print(etat_braille[i], end="")
        if i < 5:
            print("][", end="")
    print("]")


def afficher_lettre_braille(valeur):
    print("Points Braille (1-6): ", end="")
    for i in range(5, -1, -1):
        print((valeur >> i) & 1, end="")
        if i == 3:
            print(" ", end="")
    print()


def braille_to_letter_name(valeur):
    return BRAILLE_TO_LETTER.get(valeur, "?")


def next_letter(letter):
    if letter == "Z":
        return "A"
    return chr(ord(letter) + 1)


# =========================
# OLED
# =========================

def oled_show_word():
    OLED.fill(0)
    texte = " ".join(mot_affiche)
    OLED.text(texte, 20, 24)
    OLED.show()


def oled_show_success():
    OLED.fill(0)
    OLED.text("MOT OK", 36, 24)
    OLED.show()


# =========================
# Regles du jeu
# =========================

def extract_first_4_digits(serial_code):
    digits = []
    for ch in serial_code:
        if ch.isdigit():
            digits.append(ch)
        if len(digits) == 4:
            break
    return digits


def count_letters_and_digits(serial_code):
    nb_letters = 0
    nb_digits = 0
    for ch in serial_code:
        if ch.isalpha():
            nb_letters += 1
        elif ch.isdigit():
            nb_digits += 1
    return nb_letters, nb_digits


def table_letter_for_digit(digit_value, position_index):
    """
    position_index: 0..3
    Colonnes:
      pos 0 -> 1e chiffre
      pos 1 -> 2nd chiffre
      pos 2 -> 3e chiffre
      pos 3 -> 4e chiffre
    """

    if digit_value % 2 == 1 and digit_value >= 5:
        row = ["C", "A", "B", "Y"]
    elif digit_value % 2 == 1 and digit_value < 5:
        row = ["S", "U", "G", "N"]
    elif digit_value % 2 == 0 and digit_value >= 5:
        row = ["L", "I", "V", "H"]
    else:
        row = ["M", "O", "D", "X"]

    return row[position_index]


def apply_condition_1_shift_if_more_letters(serial_code, letters):
    """
    Condition 1:
    Si le code de serie contient plus de lettres que de chiffres :
    avancer l'ordre des lettres trouvees.
    Interpretation implementee:
      [L1, L2, L3, L4] -> [L2, L3, L4, L1]
    """
    nb_letters, nb_digits = count_letters_and_digits(serial_code)
    if nb_letters > nb_digits:
        return [letters[1], letters[2], letters[3], letters[0]]
    return letters


def apply_condition_2_duplicate_digits(first_4_digits, letters):
    """
    Condition 2:
    Si deux des 4 premiers chiffres sont identiques :
    remplacer la lettre correspondante aux chiffres repetes
    par la suivante dans l'alphabet.
    """
    result = letters[:]
    counts = {}

    for d in first_4_digits:
        counts[d] = counts.get(d, 0) + 1

    for i in range(4):
        d = first_4_digits[i]
        if counts.get(d, 0) >= 2:
            result[i] = next_letter(result[i])

    return result


def apply_condition_3_special_a(serial_code):
    """
    Condition 3:
    Si le code de serie se termine par 0,
    la lettre A doit etre saisie avec tous les points actifs.
    """
    return serial_code.endswith("0")


def build_word_from_serial(serial_code):
    global special_a_tous_points

    first_4_digits = extract_first_4_digits(serial_code)

    if len(first_4_digits) < 4:
        raise ValueError("Le code de serie doit contenir au moins 4 chiffres.")

    letters = []

    # Table principale
    for pos in range(4):
        digit_value = int(first_4_digits[pos])
        letters.append(table_letter_for_digit(digit_value, pos))

    # Conditions
    letters = apply_condition_1_shift_if_more_letters(serial_code, letters)
    letters = apply_condition_2_duplicate_digits(first_4_digits, letters)
    special_a_tous_points = apply_condition_3_special_a(serial_code)

    return letters


def generate_braille_targets_from_letters(letters):
    targets = []
    for letter in letters:
        if special_a_tous_points and letter == "A":
            targets.append(ALL_DOTS_ACTIVE)
        else:
            targets.append(LETTER_TO_BRAILLE[letter])
    return targets


# =========================
# Jeu
# =========================

def generer_mot(serial_code):
    global mot_lettres, mot_genere, lettre_actuelle, mot_affiche

    mot_affiche = ["_", "_", "_", "_"]
    lettre_actuelle = 0

    mot_lettres = build_word_from_serial(serial_code)
    mot_genere = generate_braille_targets_from_letters(mot_lettres)

    oled_show_word()

    print("\n" + "=" * 40)
    print("Code de serie: {}".format(serial_code))
    print("Mot a saisir: {}".format("".join(mot_lettres)))
    print("Condition A speciale: {}".format("OUI" if special_a_tous_points else "NON"))
    print("=" * 40)

    for i in range(4):
        print("Lettre {} : {}".format(i + 1, mot_lettres[i]), end="  ")
        afficher_lettre_braille(mot_genere[i])

    print("-" * 40)
    print("Saisis la lettre 1 avec les 6 boutons puis VALID")


def clignoter_led(led, duree):
    led.value(1)
    time.sleep_ms(duree)
    led.value(0)


def braille_state_to_value():
    saisie = 0
    if etat_braille[0]:
        saisie |= 0b100000
    if etat_braille[1]:
        saisie |= 0b010000
    if etat_braille[2]:
        saisie |= 0b001000
    if etat_braille[3]:
        saisie |= 0b000100
    if etat_braille[4]:
        saisie |= 0b000010
    if etat_braille[5]:
        saisie |= 0b000001
    return saisie


def main():
    global lettre_actuelle, etat_braille, mot_affiche

    LED_VERTE.value(0)
    LED_ROUGE.value(0)

    print("\n====================================")
    print(" MODULE BRAILLE ")
    print("====================================")

    generer_mot(SERIAL_CODE)

    boutons = [P1, P2, P3, P4, P5, P6]

    while True:
        maintenant = time.ticks_ms()

        for i in range(6):
            lecture = boutons[i].value()

            if lecture == 0 and dernier_etat[i] == 1:
                if time.ticks_diff(maintenant, last_debounce_time[i]) > debounce_delay:
                    etat_braille[i] ^= 1
                    afficher_etat()
                    last_debounce_time[i] = maintenant

            dernier_etat[i] = lecture

        if VALID.value() == 0:
            time.sleep_ms(50)

            saisie = braille_state_to_value()

            print("\nLettre {} saisie: ".format(lettre_actuelle + 1), end="")
            afficher_lettre_braille(saisie)

            if saisie == mot_genere[lettre_actuelle]:
                print("CORRECT !")
                clignoter_led(LED_VERTE, 300)

                mot_affiche[lettre_actuelle] = mot_lettres[lettre_actuelle]
                oled_show_word()

                lettre_actuelle += 1

                if lettre_actuelle == 4:
                    print("\nFELICITATIONS ! MOT COMPLET !")
                    print("=" * 40)

                    for _ in range(3):
                        clignoter_led(LED_VERTE, 150)
                        time.sleep_ms(150)

                    oled_show_success()
                    time.sleep_ms(1200)

                    generer_mot(SERIAL_CODE)

            else:
                print("INCORRECT ! Recommence depuis le debut !")
                clignoter_led(LED_ROUGE, 700)

                lettre_actuelle = 0
                mot_affiche = ["_", "_", "_", "_"]
                oled_show_word()

            etat_braille = [0, 0, 0, 0, 0, 0]
            afficher_etat()

            while VALID.value() == 0:
                time.sleep_ms(10)

        time.sleep_ms(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramme arrete")
        LED_VERTE.value(0)
        LED_ROUGE.value(0)
        OLED.fill(0)
        OLED.show()