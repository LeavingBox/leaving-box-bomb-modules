"""
Gestionnaire de statistiques et de progression du jeu
"""

import datetime

class GameManager:
    def __init__(self):
        self.historique = []
        self.parties_gagnees = 0
        self.parties_perdues = 0
        self.debut_session = datetime.datetime.now()
    
    def ajouter_partie(self, mode, resultat):
        """Ajoute une partie à l'historique"""
        partie = {
            'mode': mode,
            'resultat': resultat,
            'timestamp': datetime.datetime.now()
        }
        
        self.historique.append(partie)
        
        if resultat:
            self.parties_gagnees += 1
        else:
            self.parties_perdues += 1
    
    def afficher_statistiques(self):
        """Affiche les statistiques de la session"""
        total_parties = self.parties_gagnees + self.parties_perdues
        
        if total_parties == 0:
            print("Aucune partie jouée dans cette session.")
            return
        
        taux_reussite = (self.parties_gagnees / total_parties) * 100
        duree_session = datetime.datetime.now() - self.debut_session
        
        print("\n" + "📊" * 15)
        print("      STATISTIQUES DE LA SESSION")
        print("📊" * 15)
        print(f"🎮 Parties jouées: {total_parties}")
        print(f"✅ Parties gagnées: {self.parties_gagnees}")
        print(f"❌ Parties perdues: {self.parties_perdues}")
        print(f"📈 Taux de réussite: {taux_reussite:.1f}%")
        print(f"⏱️  Durée de session: {duree_session}")
        print("📊" * 15)
    
    def get_historique_recent(self, n=5):
        """Retourne les n dernières parties"""
        return self.historique[-n:]