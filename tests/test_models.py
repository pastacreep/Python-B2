import pytest
from src.models import Livre, LivreNumerique, Bibliotheque

@pytest.fixture
def livre():
    return Livre("Test Livre", "Auteur Test", "111")

@pytest.fixture
def livre_num():
    return LivreNumerique("Livre Num", "Auteur Num", "222", 10)

@pytest.fixture
def biblio(livre, livre_num):
    b = Bibliotheque()
    b.ajouter_livre(livre)
    b.ajouter_livre(livre_num)
    return b

def test_ajouter_livre(biblio, livre):
    # Le livre existe dans la bibliothèque
    titres = [l.titre for l in biblio.livres]
    assert "Test Livre" in titres

def test_supprimer_livre(biblio, livre):
    biblio.supprimer_livre_par_isbn("111")
    titres = [l.titre for l in biblio.livres]
    assert "Test Livre" not in titres

def test_rechercher_par_titre(biblio):
    result = biblio.rechercher_par_titre("Livre")
    titres = [l.titre for l in result]
    assert "Test Livre" in titres
    assert "Livre Num" in titres

def test_rechercher_par_auteur(biblio):
    result = biblio.rechercher_par_auteur("Auteur Num")
    titres = [l.titre for l in result]
    assert "Livre Num" in titres

def test_to_dict_livre(livre):
    d = livre.to_dict()
    assert d["type"] == "livre"
    assert d["titre"] == "Test Livre"
    assert d["auteur"] == "Auteur Test"

def test_to_dict_livre_numerique(livre_num):
    d = livre_num.to_dict()
    assert d["type"] == "livre_numerique"
    assert d["taille_fichier"] == 10
