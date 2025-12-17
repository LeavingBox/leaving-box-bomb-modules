import random

colors = ["Rouge", "Jaune", "Bleu", "Vert"]

# Exemple de numéro de série
serial = "HHG345DGJ"

# Déterminer la règle
def get_rule(serial):
    start = serial[0].isdigit()
    end = serial[-1].isdigit()

    if start and not end:
        return {"Bleu": "Jaune", "Jaune": "Rouge", "Vert": "Bleu", "Rouge": "Vert"}

    if start and end:
        return {"Rouge": "Jaune", "Jaune": "Bleu", "Bleu": "Vert", "Vert": "Rouge"}

    if not start and not end:
        return {"Rouge": "Bleu", "Bleu": "Rouge", "Jaune": "Vert", "Vert": "Jaune"}

    if not start and end:
        return {c: c for c in colors}


rule = get_rule(serial)
sequence = []
score = 0

print("Jeu Simon – Version Numéro de Série")
print("Numéro de série :", serial)

while True:
    new_color = random.choice(colors)
    sequence.append(new_color)

    print("\nSéquence :")
    for c in sequence:
        print(c)

    print("Entrez la séquence transformée :")
    for c in sequence:
        expected = rule[c]
        user = input(f"Pour {c} → ")

        if user != expected:
            print("Erreur ! Fin du jeu.")
            print("Score final :", score)
            quit()

    score += 1
    print("Correct ! Score :", score)
