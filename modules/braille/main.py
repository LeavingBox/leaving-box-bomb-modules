#!/usr/bin/env python3
"""
Programme principal - Jeu de détonateur avec module Braille
"""

from module_braille import ModuleBraille, module_braille_rapide
from game_manager import GameManager
import os

def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_menu_principal():
    """Affiche le menu principal"""
    print("🎮" + "="*50 + "🎮")
    print("        JEU DE DÉTONATEUR - MODULE BRAILLE")
    print("🎮" + "="*50 + "🎮")
    print("\nChoisissez un mode de jeu:")
    print("1. 🎯 Mode complet (Module Braille avancé)")
    print("2. ⚡ Mode rapide (Défi express)")
    print("3. 📚 Mode entraînement (Sans pression)")
    print("4. 🎓 Afficher l'aide Braille")
    print("5. 🚪 Quitter")
    print("\n" + "="*50)

def main():
    """Fonction principale du jeu"""
    game_manager = GameManager()
    
    while True:
        clear_screen()
        afficher_menu_principal()
        
        choix = input("\nVotre choix (1-5): ").strip()
        
        if choix == "1":
            # Mode complet
            clear_screen()
            print("🚀 Lancement du module Braille complet...")
            module = ModuleBraille()
            resultat = module.demarrer_module()
            game_manager.ajouter_partie("complet", resultat)
            
        elif choix == "2":
            # Mode rapide
            clear_screen()
            print("⚡ Lancement du mode rapide...")
            resultat = module_braille_rapide()
            game_manager.ajouter_partie("rapide", resultat)
            
        elif choix == "3":
            # Mode entraînement
            clear_screen()
            print("📚 Mode entraînement activé...")
            module = ModuleBraille()
            module.essais_restants = 999  # Essais illimités
            module.demarrer_module()
            
        elif choix == "4":
            # Aide Braille
            clear_screen()
            module = ModuleBraille()
            module.afficher_aide()
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "5":
            # Quitter
            print("\n📊 Statistiques de votre session:")
            game_manager.afficher_statistiques()
            print("\n👋 Merci d'avoir joué! À bientôt!")
            break
            
        else:
            print("❌ Choix invalide! Veuillez choisir entre 1 et 5.")
            input("Appuyez sur Entrée pour continuer...")
        
        # Pause entre les parties
        if choix in ["1", "2"]:
            input("\nAppuyez sur Entrée pour retourner au menu...")

if __name__ == "__main__":
    main()