import pytest
import os
import json
from src.file_manager import BibliothequeAvecFichier
from src.models import Livre, LivreNumerique
from src.exceptions import ErreurBibliotheque

DATA_DIR = "data"

@pytest.fixture
def biblio():
    b = BibliothequeAvecFichier()
    livre = Livre("Test Livre", "Auteur Test", "111")
    livre_num = LivreNumerique("Livre Num", "Auteur Num", "222", 10)
    b.ajouter_livre(livre)
    b.ajouter_livre(livre_num)
    return b

@pytest.fixture
def json_file():
    f = os.path.join(DATA_DIR, "test_catalogue.json")
    yield f
    if os.path.exists(f):
        os.remove(f)

@pytest.fixture
def csv_file():
    f = os.path.join(DATA_DIR, "test_catalogue.csv")
    yield f
    if os.path.exists(f):
        os.remove(f)


def test_sauvegarder_charger_json(biblio, json_file):
    # sauvegarder
    biblio.sauvegarder_json(json_file)
    assert os.path.exists(json_file)

    # vider puis charger
    biblio.livres = []
    biblio.charger_json(json_file)
    assert len(biblio.livres) == 2
    titres = [livre.titre for livre in biblio.livres]
    assert "Test Livre" in titres
    assert "Livre Num" in titres

def test_exporter_csv(biblio, csv_file):
    biblio.exporter_csv(csv_file)
    assert os.path.exists(csv_file)
    with open(csv_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Test Livre" in content
    assert "Livre Num" in content

def test_json_invalide(json_file):
    # écrire un JSON invalide
    with open(json_file, "w") as f:
        f.write("{ invalid json }")

    b = BibliothequeAvecFichier()
    with pytest.raises(ErreurBibliotheque, match="JSON invalide."):
        b.charger_json(json_file)

def test_fichier_inexistant():
    b = BibliothequeAvecFichier()
    with pytest.raises(ErreurBibliotheque, match="Le fichier n'existe pas."):
        b.charger_json("data/fichier_inexistant.json")
