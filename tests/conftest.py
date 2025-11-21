import pytest
from src.models import Livre, LivreNumerique, Bibliotheque
from src.file_manager import BibliothequeAvecFichier

@pytest.fixture
def livre_simple():
    return Livre("Test Livre", "Auteur Test", "111")

@pytest.fixture
def livre_numerique():
    return LivreNumerique("Test Num", "Auteur Num", "222", 50)

@pytest.fixture
def biblio_vide():
    return Bibliotheque()

@pytest.fixture
def biblio_fichier_tmp(tmp_path):
    """Bibliothèque avec fichiers dans un dossier temporaire pytest."""
    biblio = BibliothequeAvecFichier()
    json_path = tmp_path / "catalogue.json"
    csv_path = tmp_path / "catalogue.csv"
    return biblio, json_path, csv_path
