from src.file_manager import BibliothequeAvecFichier
from src.models import Livre, LivreNumerique
from src.exceptions import ErreurBibliotheque
from src.interface import AppBibliotheque

def main():
    biblio = BibliothequeAvecFichier()

    # Ajouter des livres
    livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "123456")
    livre2 = LivreNumerique("Python", "Jean Dupont", "987654", 12)

    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    try:
        # Sauvegarder JSON
        biblio.sauvegarder_json("data/catalogue.json")
        print("Catalogue sauvegardé en JSON.")

        # Charger JSON
        biblio.charger_json("data/catalogue.json")
        print("\nCatalogue chargé depuis JSON :")
        for livre in biblio.livres:
            print("-", livre)

        # Export CSV
        biblio.exporter_csv("data/catalogue.csv")
        print("\nCatalogue exporté en CSV.")

    except ErreurBibliotheque as e:
        print(f"Erreur bibliothèque : {e}")

if __name__ == "__main__":
    main()
    app = AppBibliotheque()
    app.run()