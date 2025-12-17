"""
Module Braille avec système basé sur Barrettes RAM et Numéro de Série
"""

import random
import time
import os
from datetime import datetime

class ModuleBraille:
    def __init__(self, barrettes_ram=None, numero_serie=None):
        # Table de conversion Braille étendue
        self.caracteres_braille = {
            'A': '⠮', 'B': '⠭', 'C': '⠯', 'D': '⠫', 'E': '⠩', 
            'F': '⠹', 'G': '⠱', 'H': '⠳', 'I': '⠪', 'J': '⠷',
            'K': '⠧', 'L': '⠺', 'M': '⠭', 'N': '⠽', 'O': '⠮',
            'P': '⠿', 'Q': '⠷', 'R': '⠻', 'S': '⠟', 'T': '⠾',
            'U': '⠍', 'V': '⠥', 'W': '⠧', 'X': '⠝', 'Y': '⠽', 'Z': '⠯',
            '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙',
            '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊'
        }
        
        # Mots thématiques étendus
        self.mots_defi = [
            "BOMBE", "ALARME", "CODE", "SECRET", "CRITIQUE", "URGENCE",
            "DANGER", "EXPLOSIF", "DESAMORCER", "TEMPS", "SECURITE",
            "FUSIBLE", "CARTEL", "SIGNAL", "CRYPTO", "ACCES", "VERROU",
            "SIRENE", "PANIQUE", "ALERTE"
        ]
        
        # Configuration Barrettes RAM et Numéro de Série
        self.barrettes_ram = barrettes_ram if barrettes_ram is not None else random.randint(0, 2)
        self.numero_serie = numero_serie if numero_serie is not None else random.randint(1000, 9999)
        
        self.generer_code_serie()
        self.analyser_configuration()
        self.reset_module()
    
    def generer_code_serie(self):
        """Génère un code de série basé sur la configuration RAM et Série"""
        # Format: RAMX-YYYY-Z (X: barrettes, YYYY: num série, Z: P/I pour Pair/Impair)
        statut_serie = "P" if self.numero_serie % 2 == 0 else "I"
        self.code_serie = f"RAM{self.barrettes_ram}-{self.numero_serie}-{statut_serie}"
    
    def analyser_configuration(self):
        """Analyse la configuration RAM et Série pour définir les conditions de jeu"""
        
        # === CONDITIONS BASÉES SUR LES BARRETTES RAM ===
        if self.barrettes_ram == 0:
            # 0 barrette → Conditions normales
            self.essais_base = 3
            self.mode_chrono = False
            self.longueur_minimale = 4
        elif self.barrettes_ram == 1:
            # 1 barrette → Conditions difficiles
            self.essais_base = 2
            self.mode_chrono = True
            self.longueur_minimale = 5
        elif self.barrettes_ram == 2:
            # 2 barrettes → Conditions très difficiles
            self.essais_base = 1
            self.mode_chrono = True
            self.longueur_minimale = 6
        
        # === CONDITIONS BASÉES SUR LE NUMÉRO DE SÉRIE ===
        if self.numero_serie % 2 == 0:
            # Série PAIRE → Aides disponibles
            self.aide_disponible = True
            self.lettres_interdites = []  # Pas de lettres interdites
            self.difficulte_mots = "FACILE"
        else:
            # Série IMPAIRE → Aides limitées
            self.aide_disponible = False
            # Lettres interdites basées sur le numéro de série
            lettres_possibles = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            index1 = (self.numero_serie // 100) % 26
            index2 = (self.numero_serie % 100) % 26
            self.lettres_interdites = [lettres_possibles[index1], lettres_possibles[index2]]
            self.difficulte_mots = "DIFFICILE"
        
        print(f"🔧 Configuration analysée: {self.barrettes_ram} RAM, Série {self.numero_serie} ({'PAIR' if self.numero_serie % 2 == 0 else 'IMPAIR'})")
    
    def afficher_configuration_boitier(self):
        """Affiche la configuration complète du boîtier"""
        print("\n" + "🎛️" * 20)
        print("        CONFIGURATION DU BOÎTIER")
        print("🎛️" * 20)
        
        print(f"\n📊 ÉTAT DU MATÉRIEL:")
        print(f"   Barrettes RAM: {self.barrettes_ram}")
        print(f"   Numéro de série: {self.numero_serie}")
        print(f"   Statut: {'PAIR' if self.numero_serie % 2 == 0 else 'IMPAIR'}")
        
        print(f"\n⚙️  CONDITIONS APPLIQUÉES:")
        conditions = self.get_conditions_jeu()
        for condition in conditions:
            print(f"   • {condition}")
        
        print("🎛️" * 20)
    
    def filtrer_mots_selon_conditions(self):
        """Filtre les mots disponibles selon les conditions RAM et Série"""
        mots_filtres = []
        
        for mot in self.mots_defi:
            # Vérifier longueur minimale (basée sur RAM)
            if len(mot) < self.longueur_minimale:
                continue
            
            # Vérifier lettres interdites (basées sur série impaire)
            if any(lettre in mot for lettre in self.lettres_interdites):
                continue
            
            # Vérifier difficulté (basée sur série)
            if self.difficulte_mots == "DIFFICILE" and len(mot) < 6:
                continue
            
            mots_filtres.append(mot)
        
        # Si aucun mot ne passe le filtre, utiliser tous les mots
        return mots_filtres if mots_filtres else self.mots_defi
    
    def get_conditions_jeu(self):
        """Retourne la description des conditions actuelles"""
        conditions = []
        
        conditions.append(f"🎯 Essais: {self.essais_base} (RAM: {self.barrettes_ram})")
        conditions.append(f"📊 Difficulté: {self.difficulte_mots} (Série: {'PAIRE' if self.numero_serie % 2 == 0 else 'IMPAIRE'})")
        conditions.append(f"💡 Aide: {'✅ OUI' if self.aide_disponible else '❌ NON'}")
        conditions.append(f"⏱️  Chrono: {'✅ ACTIVÉ' if self.mode_chrono else '❌ DÉSACTIVÉ'}")
        
        if self.lettres_interdites:
            conditions.append(f"🚫 Lettres interdites: {', '.join(self.lettres_interdites)}")
        
        conditions.append(f"📏 Longueur min: {self.longueur_minimale} lettres")
        
        return conditions
    
    def reset_module(self):
        """Réinitialise le module avec un nouveau mot selon les conditions"""
        mots_disponibles = self.filtrer_mots_selon_conditions()
        self.mot_actuel = random.choice(mots_disponibles)
        self.sequence_braille = self.convertir_en_braille(self.mot_actuel)
        self.essais_restants = self.essais_base
        self.module_active = True
        
        # Initialiser le chronomètre si activé
        if self.mode_chrono:
            self.temps_debut = time.time()
            # Temps basé sur la difficulté
            if self.barrettes_ram == 1:
                self.temps_limite = 25 + (len(self.mot_actuel) * 3)
            else:  # barrettes_ram == 2
                self.temps_limite = 20 + (len(self.mot_actuel) * 2)
    
    def convertir_en_braille(self, mot):
        """Convertit un mot en séquence Braille"""
        return [self.caracteres_braille.get(lettre, '?') for lettre in mot.upper()]
    
    def afficher_entete_jeu(self):
        """Affiche l'en-tête du jeu avec la configuration et conditions"""
        print("\n" + "═" * 60)
        print("           🚨 MODULE BRAILLE - DÉTONATEUR")
        print("═" * 60)
        print(f"🔢 CONFIGURATION: {self.code_serie}")
        print(f"📋 Séquence Braille: {'   '.join(self.sequence_braille)}")
        print(f"🎯 Longueur du mot: {len(self.mot_actuel)} caractères")
        print(f"💡 Essais restants: {self.essais_restants}")
        
        # Afficher le temps restant si mode chrono
        if self.mode_chrono:
            temps_ecoule = time.time() - self.temps_debut
            temps_restant = max(0, self.temps_limite - temps_ecoule)
            print(f"⏱️  Temps restant: {int(temps_restant)} secondes")
        
        if self.lettres_interdites:
            print(f"🚫 Lettres interdites: {', '.join(self.lettres_interdites)}")
        
        print("═" * 60)
    
    def verifier_temps_ecoule(self):
        """Vérifie si le temps est écoulé en mode chrono"""
        if self.mode_chrono:
            temps_ecoule = time.time() - self.temps_debut
            return temps_ecoule > self.temps_limite
        return False
    
    def verifier_reponse(self, reponse):
        """Vérifie si la réponse est correcte avec conditions spéciales"""
        if self.verifier_temps_ecoule():
            print("⏰ TEMPS ÉCOULÉ! DÉTONATION!")
            self.essais_restants = 0
            return False
        
        reponse_clean = reponse.upper().strip()
        
        # Vérifier lettres interdites (série impaire)
        if any(lettre in reponse_clean for lettre in self.lettres_interdites):
            print(f"🚫 ERREUR: Lettre(s) interdite(s) utilisée(s): {', '.join(self.lettres_interdites)}")
            self.essais_restants -= 1
            return False
        
        if reponse_clean == self.mot_actuel:
            return True
        else:
            self.essais_restants -= 1
            return False
    
    def afficher_aide(self):
        """Affiche l'aide Braille (si disponible selon configuration)"""
        if not self.aide_disponible:
            print("\n❌ AIDE INDISPONIBLE - Série impaire détectée")
            print("💡 Vous devez résoudre sans assistance!")
            return
        
        print("\n" + "▄" * 50)
        print("            🎓 AIDE - CODE BRAILLE")
        print("▄" * 50)
        
        # Afficher seulement les lettres non interdites
        lettres_a_afficher = []
        for lettre, braille in self.caracteres_braille.items():
            if lettre not in self.lettres_interdites and lettre.isalpha():
                lettres_a_afficher.append((lettre, braille))
        
        # Afficher en colonnes
        for i in range(0, len(lettres_a_afficher), 6):
            ligne = ""
            for lettre, braille in lettres_a_afficher[i:i+6]:
                ligne += f"  {lettre}: {braille}"
            print(ligne)
        
        if self.lettres_interdites:
            print(f"\n🚫 Lettres interdites: {', '.join(self.lettres_interdites)}")
        
        print("▄" * 50)
    
    def afficher_conditions_serie(self):
        """Affiche les conditions imposées par la configuration"""
        print("\n" + "🔧" * 20)
        print("   CONDITIONS DE CONFIGURATION")
        print("🔧" * 20)
        
        conditions = self.get_conditions_jeu()
        for condition in conditions:
            print(f"  • {condition}")
        
        print("🔧" * 20)
    
    def donner_indice(self):
        """Donne un indice (si disponible selon configuration)"""
        if not self.aide_disponible:
            print("❌ Indices désactivés - Série impaire!")
            return
        
        indices = [
            f"Le mot commence par '{self.mot_actuel[0]}'",
            f"Le mot contient {len(self.mot_actuel)} lettres",
            f"La deuxième lettre est '{self.mot_actuel[1]}'",
            f"Le mot se termine par '{self.mot_actuel[-1]}'",
            f"Le mot contient la lettre '{random.choice(self.mot_actuel[1:-1])}'"
        ]
        
        print(f"\n💡 Indice: {random.choice(indices)}")
    
    def demarrer_module(self):
        """Lance le module Braille avec conditions de configuration"""
        print("\n🔄 Analyse de la configuration du boîtier...")
        time.sleep(1)
        
        self.afficher_configuration_boitier()
        input("\nAppuyez sur Entrée pour continuer...")
        
        while self.module_active and self.essais_restants > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.afficher_entete_jeu()
            
            # Vérifier temps écoulé
            if self.verifier_temps_ecoule():
                print("💥 DÉTONATION! Temps écoulé!")
                return False
            
            print("\n📝 Options disponibles:")
            print("1. 💾 Saisir la réponse")
            if self.aide_disponible:
                print("2. 🎓 Aide Braille")
                print("3. 💡 Demander un indice")
            else:
                print("2. 🚫 Aide Braille (DÉSACTIVÉ)")
                print("3. 🚫 Indice (DÉSACTIVÉ)")
            print("4. 🔧 Afficher configuration")
            print("5. 🔄 Nouvelle configuration")
            print("6. 🏠 Retour menu principal")
            
            choix = input("\n🎮 Votre choix: ").strip()
            
            if choix == "1":
                reponse = input("\n🔤 Entrez le mot décodé: ").strip()
                
                if self.verifier_reponse(reponse):
                    print(f"\n✅ SUCCÈS! Le mot '{self.mot_actuel}' était correct!")
                    print("🎉 Module désamorcé avec succès!")
                    self.module_active = False
                    return True
                else:
                    if self.essais_restants <= 0:
                        print("💥 DÉTONATION! Trop d'échecs!")
                        return False
            
            elif choix == "2" and self.aide_disponible:
                self.afficher_aide()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "3" and self.aide_disponible:
                self.donner_indice()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                self.afficher_configuration_boitier()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "5":
                # Nouvelle configuration aléatoire
                self.barrettes_ram = random.randint(0, 2)
                self.numero_serie = random.randint(1000, 9999)
                self.generer_code_serie()
                self.analyser_configuration()
                self.reset_module()
                print("🔄 Nouvelle configuration générée!")
                self.afficher_configuration_boitier()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                print("🚪 Retour au menu principal...")
                return None
            
            else:
                print("❌ Choix invalide ou option désactivée!")
                time.sleep(1)
        
        return False

# Fonction pour créer un module avec configuration manuelle
def creer_module_braille_manuel():
    """Crée un module Braille avec configuration manuelle"""
    print("\n🎛️  CONFIGURATION MANUELLE DU BOÎTIER")
    print("═" * 40)
    
    try:
        barrettes = int(input("Barrettes RAM (0, 1 ou 2): "))
        if barrettes not in [0, 1, 2]:
            barrettes = 0
            print("⚠️  Valeur invalide, utilisation de 0 par défaut")
    except:
        barrettes = 0
        print("⚠️  Entrée invalide, utilisation de 0 par défaut")
    
    try:
        serie = int(input("Numéro de série (1000-9999): "))
        if not 1000 <= serie <= 9999:
            serie = random.randint(1000, 9999)
            print(f"⚠️  Valeur invalide, utilisation de {serie} par défaut")
    except:
        serie = random.randint(1000, 9999)
        print(f"⚠️  Entrée invalide, utilisation de {serie} par défaut")
    
    return ModuleBraille(barrettes_ram=barrettes, numero_serie=serie)

# Version rapide avec configuration aléatoire
def module_braille_rapide():
    """Version rapide avec configuration aléatoire"""
    module = ModuleBraille()
    
    # Mode rapide : conditions renforcées
    if module.mode_chrono:
        module.temps_limite = max(15, module.temps_limite // 2)
    else:
        module.mode_chrono = True
        module.temps_limite = 20
    
    module.temps_debut = time.time()
    
    print("\n⚡ MODE RAPIDE BRAILLE")
    print("═" * 40)
    module.afficher_configuration_boitier()
    print(f"⏱️  Temps limité: {module.temps_limite} secondes")
    print("═" * 40)
    
    for essai in range(module.essais_base):
        if module.mode_chrono and (time.time() - module.temps_debut > module.temps_limite):
            print("⏰ TEMPS ÉCOULÉ!")
            return False
            
        reponse = input(f"\nEssai {essai + 1}/{module.essais_base}: ").upper().strip()
        
        if module.verifier_reponse(reponse):
            print("✅ Module désamorcé!")
            return True
        else:
            if module.mode_chrono:
                temps_restant = module.temps_limite - (time.time() - module.temps_debut)
                print(f"❌ Incorrect! Temps restant: {int(temps_restant)}s")
    
    print("💥 DÉTONATION!")
    return False

# Test
if __name__ == "__main__":
    print("Test du module Braille avec configuration RAM/Série...")
    module = ModuleBraille(barrettes_ram=1, numero_serie=1234)
    module.demarrer_module()