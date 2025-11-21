# file_manager.py
import json
import csv
import os

from src.models import Bibliotheque, Livre, LivreNumerique
from src.exceptions import ErreurBibliotheque


class BibliothequeAvecFichier(Bibliotheque):

    # Sauvegarde JSON
    def sauvegarder_json(self, fichier):
        try:
            data = [livre.to_dict() for livre in self.livres]

            with open(fichier, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"Catalogue sauvegardé dans {fichier}")

        except Exception as e:
            raise ErreurBibliotheque(f"Erreur lors de la sauvegarde JSON : {e}")


    # Chargement JSON
    def charger_json(self, fichier):
        if not os.path.exists(fichier):
            raise ErreurBibliotheque("Le fichier n'existe pas.")

        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.livres = []
            for item in data:
                if item["type"] == "livre":
                    self.livres.append(Livre(item["titre"], item["auteur"], item["isbn"]))
                elif item["type"] == "livre_numerique":
                    self.livres.append(LivreNumerique(
                        item["titre"], item["auteur"], item["isbn"], item["taille_fichier"]
                    ))
                else:
                    raise ErreurBibliotheque("Type de livre inconnu dans le JSON.")

        except json.JSONDecodeError:
            raise ErreurBibliotheque("JSON invalide.")
        except Exception as e:
            raise ErreurBibliotheque(f"Erreur lors du chargement JSON : {e}")


    # Export CSV
    def exporter_csv(self, fichier):
        try:
            with open(fichier, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["titre", "auteur", "isbn", "type", "taille_fichier"])

                for livre in self.livres:
                    if isinstance(livre, LivreNumerique):
                        writer.writerow([livre.titre, livre.auteur, livre.isbn, "numerique", livre.taille_fichier])
                    else:
                        writer.writerow([livre.titre, livre.auteur, livre.isbn, "papier", ""])

        except Exception as e:
            raise ErreurBibliotheque(f"Erreur lors de l'export CSV : {e}")
