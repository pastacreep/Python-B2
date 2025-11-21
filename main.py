from src.file_manager import BibliothequeAvecFichier
from src.models import Livre, LivreNumerique, Utilisateur
from src.exceptions import ErreurBibliotheque
from src.interface import AppBibliotheque

def main():
    biblio = BibliothequeAvecFichier()


    # ---- Charger JSON existant ----
    try:
        biblio.charger_json("data/catalogue.json")
        print("Catalogue chargé depuis JSON.")
    except ErreurBibliotheque as e:
        print(f"Erreur bibliothèque : {e}")

    # ---- Emprunter des livres (seul les non-admins) ----
    for u in biblio.utilisateurs:
        if not u.admin:
            if u.username == "michel":
                biblio.emprunter_livre(u.username, "123456")
            elif u.username == "michelle":
                biblio.emprunter_livre(u.username, "987654")

    # ---- Affichage général ----
    print("\n=== Bibliothèque ===")
    for livre in biblio.livres:
        print("-", livre)

    print("\n=== Historique d'emprunts ===")
    for u in biblio.utilisateurs:
        if u.admin:
            # Admin voit tous les livres et utilisateurs
            print(f"\n{u.username} (Admin) voit tous les livres :")
            for livre in biblio.livres:
                status = f", emprunté par {livre.emprunte_par.username}" if livre.emprunte_par else ""
                print(f"- {livre.titre} ({livre.isbn}{status})")
        else:
            print(u.afficher_historique())


    # Créer des utilisateurs
    admin = Utilisateur("admin", "admin", admin=True)
    michel = Utilisateur("michel", "123456", admin=False)
    michelle = Utilisateur("michelle", "123456", admin=False)

    biblio.ajouter_utilisateur(admin)
    biblio.ajouter_utilisateur(michel)
    biblio.ajouter_utilisateur(michelle)

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

        # ---- Emprunt de livre ----
        biblio.emprunter_livre("michel", "123456")
        biblio.emprunter_livre("michelle", "987654")

        # ---- Vérification emprunt ----
        print("\nAprès emprunts :")
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