import json
import csv
import os
from src.models import Bibliotheque, Livre, LivreNumerique, Utilisateur
from src.exceptions import ErreurBibliotheque

class BibliothequeAvecFichier(Bibliotheque):
    def __init__(self):
        super().__init__()
        self.fichier_json = "data/catalogue.json"

    # ---- Sauvegarde JSON ----
    def sauvegarder_json(self, fichier=None):
        if fichier is None:
            fichier = self.fichier_json
        try:
            dossier = os.path.dirname(fichier)
            if not os.path.exists(dossier):
                os.makedirs(dossier)

            data = {
                "livres": [livre.to_dict() for livre in self.livres],
                "utilisateurs": [
                    {
                        "username": u.username,
                        "mdp": u.mdp,
                        "admin": u.admin,
                        "livres_empruntes": [l.isbn for l in u.livres_empruntes],
                        "historique_emprunts": [l.isbn for l in u.historique_emprunts]
                    }
                    for u in self.utilisateurs
                ]
            }
            with open(fichier, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Catalogue sauvegardé dans {fichier}")
        except Exception as e:
            raise ErreurBibliotheque(f"Erreur lors de la sauvegarde JSON : {e}")

    # ---- Chargement JSON ----
    def charger_json(self, fichier=None):
        if fichier is None:
            fichier = self.fichier_json

        if not os.path.exists(fichier):
            print("Fichier JSON introuvable. Nouveau catalogue créé.")
            self.livres = []
            self.utilisateurs = []
            return
        
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)

            # ---- Charger les livres ----
            self.livres = []
            for item in data.get("livres", []):
                if item["type"] == "livre_numerique":
                    livre = LivreNumerique(item["titre"], item["auteur"], item["isbn"], item["taille_fichier"])
                else:
                    livre = Livre(item["titre"], item["auteur"], item["isbn"])
                self.livres.append(livre)

            # ---- Charger les utilisateurs ----
            self.utilisateurs = []
            for u in data.get("utilisateurs", []):
                user = Utilisateur(u["username"], u["mdp"], u["admin"])

                # Associer les livres actuellement empruntés
                for isbn in u.get("livres_empruntes", []):
                    livre_emprunte = next((l for l in self.livres if l.isbn == isbn), None)
                    if livre_emprunte:
                        livre_emprunte.emprunte_par = user
                        user.livres_empruntes.append(livre_emprunte)

                # Associer l’historique d’emprunts
                for isbn in u.get("historique_emprunts", []):
                    livre_historique = next((l for l in self.livres if l.isbn == isbn), None)
                    if livre_historique and livre_historique not in user.historique_emprunts:
                        user.historique_emprunts.append(livre_historique)

                self.utilisateurs.append(user)

        except Exception as e:
            raise ErreurBibliotheque(f"Erreur chargement JSON : {e}")

    # ---- Export CSV ----
    def exporter_csv(self, fichier):
        try:
            with open(fichier, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["titre", "auteur", "isbn", "type", "taille_fichier", "emprunte_par"])

                for livre in self.livres:
                    type_livre = "Numérique" if isinstance(livre, LivreNumerique) else "Papier"
                    taille = getattr(livre, "taille_fichier", "")
                    emprunte_par = livre.emprunte_par.username if livre.emprunte_par else ""
                    writer.writerow([livre.titre, livre.auteur, livre.isbn, type_livre, taille, emprunte_par])
        except Exception as e:
            raise ErreurBibliotheque(f"Erreur export CSV : {e}")
