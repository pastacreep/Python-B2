class Livre:
    def __init__(self, titre, auteur, isbn):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.emprunte_par = None  # Référence à l'utilisateur qui a emprunté le livre

    def __str__(self):
        status = f", emprunté par {self.emprunte_par.username}" if self.emprunte_par else ""
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn}{status})"

    def to_dict(self):
        return {
            "type": "livre",
            "titre": self.titre,
            "auteur": self.auteur,
            "isbn": self.isbn,
            "emprunte_par": self.emprunte_par.username if self.emprunte_par else None
        }


class LivreNumerique(Livre):
    def __init__(self, titre, auteur, isbn, taille_fichier):
        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    def __str__(self):
        status = f", emprunté par {self.emprunte_par.username}" if self.emprunte_par else ""
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn}, {self.taille_fichier} Mo{status})"

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "livre_numerique"
        d["taille_fichier"] = self.taille_fichier
        return d


class Utilisateur:
    def __init__(self, username, mdp, admin=False):
        self.username = username
        self.mdp = mdp
        self.admin = admin
        self.livres_empruntes = []           # Livres actuellement empruntés
        self.historique_emprunts = []        # Tous les livres déjà empruntés

    def __str__(self):
        role = "Admin" if self.admin else "Utilisateur"
        return f"{self.username} ({role})"

    def afficher_historique(self):
        if not self.historique_emprunts:
            return f"Aucun emprunt pour {self.username}."

        historique = f"Historique d'emprunts de {self.username} :\n"
        for livre in self.historique_emprunts:
            historique += f"- {livre.titre} ({livre.isbn})\n"
        return historique.strip()

    def afficher_emprunts_actuels(self):
        if not self.livres_empruntes:
            return f"{self.username} n’a emprunté aucun livre."
        emprunts = f"Livres actuellement empruntés par {self.username} :\n"
        for livre in self.livres_empruntes:
            emprunts += f"- {livre.titre} ({livre.isbn})\n"
        return emprunts.strip()


class Bibliotheque:
    def __init__(self):
        self.livres = []         # Liste de livres
        self.utilisateurs = []   # Liste d'utilisateurs

    # ---- Gestion livres ----
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

    # ---- Gestion utilisateurs ----
    def ajouter_utilisateur(self, user):
        self.utilisateurs.append(user)
        print(f"Utilisateur '{user.username}' ajouté.")

    def trouver_utilisateur(self, username):
        for u in self.utilisateurs:
            if u.username == username:
                return u
        return None

    # ---- Gestion emprunts ----
    def emprunter_livre(self, username, isbn):
        user = self.trouver_utilisateur(username)
        if not user:
            print("Utilisateur introuvable.")
            return

        livre = next((l for l in self.livres if l.isbn == isbn), None)
        if not livre:
            print("Livre introuvable.")
            return

        if livre.emprunte_par:
            print(f"Le livre '{livre.titre}' est déjà emprunté par {livre.emprunte_par.username}.")
            return

        # Emprunt
        livre.emprunte_par = user
        user.livres_empruntes.append(livre)

        # Ajout à l’historique
        user.historique_emprunts.append(livre)

        print(f"Le livre '{livre.titre}' a été emprunté par {user.username}.")

    def rendre_livre(self, username, isbn):
        user = self.trouver_utilisateur(username)
        if not user:
            print("Utilisateur introuvable.")
            return

        livre = next((l for l in user.livres_empruntes if l.isbn == isbn), None)
        if not livre:
            print(f"{user.username} n'a pas emprunté ce livre.")
            return

        livre.emprunte_par = None
        user.livres_empruntes.remove(livre)

        print(f"Le livre '{livre.titre}' a été rendu par {user.username}.")
