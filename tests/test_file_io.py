import os
import json
import csv
import pytest
from src.file_manager import BibliothequeAvecFichier
from src.models import Livre, LivreNumerique, Utilisateur
from src.exceptions import ErreurBibliotheque

DATA_JSON = "test_data/catalogue.json"
DATA_CSV = "test_data/catalogue.csv"

@pytest.fixture
def biblio():
    # Créer une instance propre pour chaque test
    b = BibliothequeAvecFichier()
    b.fichier_json = DATA_JSON
    # Nettoyer le dossier test_data
    if os.path.exists("test_data"):
        for f in os.listdir("test_data"):
            os.remove(os.path.join("test_data", f))
    else:
        os.makedirs("test_data")
    return b

def test_ajout_utilisateurs_et_livres(biblio):
    admin = Utilisateur("admin", "admin", True)
    user = Utilisateur("michel", "123456", False)
    livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "123")
    livre2 = LivreNumerique("Python", "Jean Dupont", "456", 12)

    biblio.ajouter_utilisateur(admin)
    biblio.ajouter_utilisateur(user)
    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    assert len(biblio.utilisateurs) == 2
    assert len(biblio.livres) == 2

def test_emprunt_et_retour(biblio):
    user = Utilisateur("michel", "123456")
    livre = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "123")
    biblio.ajouter_utilisateur(user)
    biblio.ajouter_livre(livre)

    biblio.emprunter_livre("michel", "123")
    assert livre.emprunte_par == user
    assert livre in user.livres_empruntes
    assert livre in user.historique_emprunts

    biblio.rendre_livre("michel", "123")
    assert livre.emprunte_par is None
    assert livre not in user.livres_empruntes

def test_sauvegarde_et_chargement_json(biblio):
    user = Utilisateur("michel", "123456")
    livre = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "123")
    biblio.ajouter_utilisateur(user)
    biblio.ajouter_livre(livre)
    biblio.emprunter_livre("michel", "123")

    # Sauvegarde
    biblio.sauvegarder_json(DATA_JSON)
    assert os.path.exists(DATA_JSON)

    # Nouvelle instance pour tester le chargement
    biblio2 = BibliothequeAvecFichier()
    biblio2.fichier_json = DATA_JSON
    biblio2.charger_json()
    assert len(biblio2.livres) == 1
    assert len(biblio2.utilisateurs) == 1
    livre_charge = biblio2.livres[0]
    user_charge = biblio2.utilisateurs[0]
    assert livre_charge.emprunte_par.username == "michel"
    assert livre_charge in user_charge.livres_empruntes
    assert livre_charge in user_charge.historique_emprunts

def test_export_csv(biblio):
    user = Utilisateur("michel", "123456")
    livre = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "123")
    biblio.ajouter_utilisateur(user)
    biblio.ajouter_livre(livre)
    biblio.emprunter_livre("michel", "123")

    biblio.exporter_csv(DATA_CSV)
    assert os.path.exists(DATA_CSV)

    # Vérifier que le contenu CSV contient la ligne du livre
    with open(DATA_CSV, "r", encoding="utf-8") as f:
        lignes = list(csv.reader(f))
        # En-tête + 1 livre
        assert len(lignes) == 2
        assert lignes[1][0] == "Le Petit Prince"
        assert lignes[1][-1] == "michel"
