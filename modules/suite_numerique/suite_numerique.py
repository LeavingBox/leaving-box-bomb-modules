# ==============================
# MODULE : SUITE NUMERIQUE
# ==============================

def count_serial(serial):
    digits = [c for c in serial if c.isdigit()]
    letters = [c for c in serial if c.isalpha()]

    even = [d for d in digits if int(d) % 2 == 0]
    odd = [d for d in digits if int(d) % 2 != 0]

    vowels = [l for l in letters if l.lower() in "aeiouy"]
    consonants = [l for l in letters if l.lower() not in "aeiouy"]

    return {
        "digits": len(digits),
        "letters": len(letters),
        "even": len(even),
        "odd": len(odd),
        "vowels": len(vowels),
        "consonants": len(consonants)
    }


def condition_1(stats, ram):
    if stats["digits"] > stats["letters"]:
        return {1: "61", 2: "04", 3: "27", 4: "67"}[ram]
    else:
        return {1: "34", 2: "99", 3: "87", 4: "22"}[ram]


def condition_2(stats, ram):
    if stats["even"] == stats["odd"]:
        return {1: "42", 2: "82", 3: "96"}[ram]
    else:
        return {1: "17", 2: "88", 3: "43", 4: "09"}[ram]


def condition_3(stats, ram):
    if stats["vowels"] > stats["consonants"]:
        return {1: "02", 2: "06", 3: "03", 4: "47"}[ram]
    else:
        return {1: "55", 2: "41", 3: "95", 4: "93"}[ram]


def suite_numerique(serial, ram):
    stats = count_serial(serial)

    part1 = condition_1(stats, ram)
    part2 = condition_2(stats, ram)
    part3 = condition_3(stats, ram)

    return part1 + part2 + part3
if __name__ == "__main__":
    serial = input("Entrez le numéro de série : ")
    ram = int(input("Nombre de barrettes RAM (1 à 4) : "))

    code = suite_numerique(serial, ram)
    print("Code généré :", code)
