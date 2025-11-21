import tkinter as tk
from tkinter import ttk, messagebox
from src.models import Livre, LivreNumerique
from src.file_manager import BibliothequeAvecFichier
from src.exceptions import ErreurBibliotheque


class AppBibliotheque:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Gestion Bibliothèque")
        self.biblio = BibliothequeAvecFichier()
        self.fichier_json = "data/catalogue.json"

        self.creer_widgets()
        self.charger_livres_depuis_fichier()

    def creer_widgets(self):
        # ---- Formulaire ajout livre ----
        frame_inputs = ttk.LabelFrame(self.fenetre, text="Ajouter un livre")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_inputs, text="Titre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_titre = ttk.Entry(frame_inputs)
        self.entry_titre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Auteur:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_auteur = ttk.Entry(frame_inputs)
        self.entry_auteur.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="ISBN:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_isbn = ttk.Entry(frame_inputs)
        self.entry_isbn.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Taille fichier (Mo, optionnel):").grid(row=3, column=0, padx=5, pady=5)
        self.entry_taille = ttk.Entry(frame_inputs)
        self.entry_taille.grid(row=3, column=1, padx=5, pady=5)

        btn_ajouter = ttk.Button(frame_inputs, text="Ajouter Livre", command=self.ajouter_livre)
        btn_ajouter.grid(row=4, column=0, columnspan=2, pady=10)

        # ---- Recherche par auteur ----
        frame_recherche = ttk.LabelFrame(self.fenetre, text="Recherche par auteur")
        frame_recherche.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_recherche, text="Auteur:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_recherche = ttk.Entry(frame_recherche)
        self.entry_recherche.grid(row=0, column=1, padx=5, pady=5)
        btn_recherche = ttk.Button(frame_recherche, text="Rechercher", command=self.rechercher_auteur)
        btn_recherche.grid(row=0, column=2, padx=5, pady=5)

        # ---- Affichage des livres ----
        frame_view = ttk.LabelFrame(self.fenetre, text="Livres enregistrés")
        frame_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_view, columns=("Titre", "Auteur", "ISBN", "Type", "Taille"), show="headings")
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Auteur", text="Auteur")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Taille", text="Taille fichier (Mo)")
        self.tree.pack(fill="both", expand=True)

    # ---- Gestion ajout livre avec sauvegarde ----
    def ajouter_livre(self):
        titre = self.entry_titre.get().strip()
        auteur = self.entry_auteur.get().strip()
        isbn = self.entry_isbn.get().strip()
        taille = self.entry_taille.get().strip()

        if not titre or not auteur or not isbn:
            messagebox.showerror("Erreur", "Titre, Auteur et ISBN sont obligatoires")
            return

        if taille:
            try:
                taille = float(taille)
                livre = LivreNumerique(titre, auteur, isbn, taille)
            except ValueError:
                messagebox.showerror("Erreur", "Taille fichier doit être un nombre")
                return
        else:
            livre = Livre(titre, auteur, isbn)

        self.biblio.ajouter_livre(livre)
        try:
            self.biblio.sauvegarder_json(self.fichier_json)
        except ErreurBibliotheque as e:
            messagebox.showerror("Erreur sauvegarde", str(e))

        self.charger_livres()
        self.entry_titre.delete(0, tk.END)
        self.entry_auteur.delete(0, tk.END)
        self.entry_isbn.delete(0, tk.END)
        self.entry_taille.delete(0, tk.END)

    # ---- Chargement livres depuis fichier JSON ----
    def charger_livres_depuis_fichier(self):
        try:
            self.biblio.charger_json(self.fichier_json)
        except ErreurBibliotheque as e:
            messagebox.showwarning("Attention", f"Impossible de charger le fichier : {e}")
        self.charger_livres()

    # ---- Affichage livres dans Treeview ----
    def charger_livres(self, livres=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if livres is None:
            livres = self.biblio.livres

        for livre in livres:
            if isinstance(livre, LivreNumerique):
                type_livre = "Numérique"
                taille = livre.taille_fichier
            else:
                type_livre = "Papier"
                taille = ""
            self.tree.insert("", "end", values=(livre.titre, livre.auteur, livre.isbn, type_livre, taille))

    # ---- Recherche par auteur ----
    def rechercher_auteur(self):
        auteur = self.entry_recherche.get().strip()
        if not auteur:
            self.charger_livres()
            return
        resultats = self.biblio.rechercher_par_auteur(auteur)
        self.charger_livres(resultats)

    def run(self):
        self.fenetre.mainloop()


if __name__ == "__main__":
    AppBibliotheque().run()
