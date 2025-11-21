class Livre:
    def __init__(self, titre, auteur, isbn):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn

    def __str__(self):
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn})"

    def to_dict(self):
        return {
            "type": "livre",
            "titre": self.titre,
            "auteur": self.auteur,
            "isbn": self.isbn
        }


class LivreNumerique(Livre):
    def __init__(self, titre, auteur, isbn, taille_fichier):
        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier  

    def __str__(self):
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn}, {self.taille_fichier} Mo)"

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "livre_numerique"
        d["taille_fichier"] = self.taille_fichier
        return d


class Bibliotheque:
    def __init__(self):
        self.livres = []  # liste d'objets Livre / LivreNumerique

    def ajouter_livre(self, livre):
        self.livres.append(livre)
        print(f"Livre '{livre.titre}' ajouté.")

    def supprimer_livre_par_isbn(self, isbn):
        for livre in self.livres:
            if livre.isbn == isbn:
                self.livres.remove(livre)
                print(f"Livre '{livre.titre}' supprimé.")
                return
        print("Livre non trouvé.")

    def rechercher_par_titre(self, titre):
        return [l for l in self.livres if titre.lower() in l.titre.lower()]

    def rechercher_par_auteur(self, auteur):
        return [l for l in self.livres if auteur.lower() in l.auteur.lower()]
