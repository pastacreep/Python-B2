import tkinter as tk
from tkinter import ttk, messagebox
from src.models import Livre, LivreNumerique, Utilisateur
from src.file_manager import BibliothequeAvecFichier
from src.exceptions import ErreurBibliotheque

class AppBibliotheque:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Gestion Bibliothèque")
        self.fenetre.geometry("800x600")

        self.biblio = BibliothequeAvecFichier()
        self.fichier_json = "data/catalogue.json"

        # Onglets
        self.notebook = ttk.Notebook(self.fenetre)
        self.notebook.pack(fill="both", expand=True)

        self.frame_livres = ttk.Frame(self.notebook)
        self.frame_utilisateurs = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_livres, text="Livres")
        self.notebook.add(self.frame_utilisateurs, text="Utilisateurs")

        self.creer_widgets_livres()
        self.creer_widgets_utilisateurs()
        self.charger_livres_depuis_fichier()
        self.charger_utilisateurs_depuis_fichier()

    # -------------------- Livres --------------------
    def creer_widgets_livres(self):
        frame_inputs = ttk.LabelFrame(self.frame_livres, text="Ajouter un livre")
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

        # Recherche par auteur
        frame_recherche = ttk.LabelFrame(self.frame_livres, text="Recherche par auteur")
        frame_recherche.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_recherche, text="Auteur:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_recherche = ttk.Entry(frame_recherche)
        self.entry_recherche.grid(row=0, column=1, padx=5, pady=5)
        btn_recherche = ttk.Button(frame_recherche, text="Rechercher", command=self.rechercher_auteur)
        btn_recherche.grid(row=0, column=2, padx=5, pady=5)

        # Affichage des livres
        frame_view = ttk.LabelFrame(self.frame_livres, text="Livres enregistrés")
        frame_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_livres = ttk.Treeview(frame_view, columns=("Titre", "Auteur", "ISBN", "Type", "Taille"), show="headings")
        self.tree_livres.heading("Titre", text="Titre")
        self.tree_livres.heading("Auteur", text="Auteur")
        self.tree_livres.heading("ISBN", text="ISBN")
        self.tree_livres.heading("Type", text="Type")
        self.tree_livres.heading("Taille", text="Taille fichier (Mo)")
        self.tree_livres.pack(fill="both", expand=True)

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

    def charger_livres_depuis_fichier(self):
        try:
            self.biblio.charger_json(self.fichier_json)
        except ErreurBibliotheque as e:
            messagebox.showwarning("Attention", f"Impossible de charger le fichier : {e}")
        self.charger_livres()

    def charger_livres(self, livres=None):
        for i in self.tree_livres.get_children():
            self.tree_livres.delete(i)

        if livres is None:
            livres = self.biblio.livres

        for livre in livres:
            if isinstance(livre, LivreNumerique):
                type_livre = "Numérique"
                taille = livre.taille_fichier
            else:
                type_livre = "Papier"
                taille = ""
            self.tree_livres.insert("", "end", values=(livre.titre, livre.auteur, livre.isbn, type_livre, taille))

    def rechercher_auteur(self):
        auteur = self.entry_recherche.get().strip()
        if not auteur:
            self.charger_livres()
            return
        resultats = self.biblio.rechercher_par_auteur(auteur)
        self.charger_livres(resultats)

    # -------------------- Utilisateurs --------------------
    def creer_widgets_utilisateurs(self):
        frame_form = ttk.LabelFrame(self.frame_utilisateurs, text="Ajouter un utilisateur")
        frame_form.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_form, text="Nom d'utilisateur:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = ttk.Entry(frame_form)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Mot de passe:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_mdp = ttk.Entry(frame_form, show="*")
        self.entry_mdp.grid(row=1, column=1, padx=5, pady=5)

        self.is_admin_var = tk.BooleanVar()
        ttk.Checkbutton(frame_form, text="Administrateur", variable=self.is_admin_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        ttk.Label(frame_form, text="Type abonnement:").grid(row=3, column=0, padx=5, pady=5)
        self.combo_abonnement = ttk.Combobox(frame_form, values=["basique", "premium", "VIP"])
        self.combo_abonnement.current(0)
        self.combo_abonnement.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame_form, text="Ajouter", command=self.ajouter_utilisateur).grid(row=4, column=0, columnspan=2, pady=10)

        frame_table = ttk.LabelFrame(self.frame_utilisateurs, text="Utilisateurs existants")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_utilisateurs = ttk.Treeview(frame_table, columns=("Username", "Admin", "Abonnement"), show="headings")
        self.tree_utilisateurs.heading("Username", text="Nom d'utilisateur")
        self.tree_utilisateurs.heading("Admin", text="Administrateur")
        self.tree_utilisateurs.heading("Abonnement", text="Type d'abonnement")
        self.tree_utilisateurs.pack(fill="both", expand=True)

        self.charger_utilisateurs()

    def ajouter_utilisateur(self):
        username = self.entry_username.get().strip()
        mdp = self.entry_mdp.get().strip()
        admin = self.is_admin_var.get()
        abonnement = self.combo_abonnement.get()

        if not username or not mdp:
            messagebox.showerror("Erreur", "Nom d'utilisateur et mot de passe obligatoires")
            return

        if any(u.username == username for u in self.biblio.utilisateurs):
            messagebox.showerror("Erreur", "Cet utilisateur existe déjà")
            return

        user = Utilisateur(username, mdp, admin, abonnement)
        self.biblio.ajouter_utilisateur(user)

        try:
            self.biblio.sauvegarder_json(self.fichier_json)
        except ErreurBibliotheque as e:
            messagebox.showerror("Erreur sauvegarde", str(e))
            return

        self.charger_utilisateurs()
        self.entry_username.delete(0, tk.END)
        self.entry_mdp.delete(0, tk.END)
        self.is_admin_var.set(False)
        self.combo_abonnement.current(0)

    def charger_utilisateurs_depuis_fichier(self):
        try:
            self.biblio.charger_json(self.fichier_json)
        except ErreurBibliotheque as e:
            messagebox.showwarning("Attention", f"Impossible de charger les utilisateurs : {e}")

    def charger_utilisateurs(self):
        for i in self.tree_utilisateurs.get_children():
            self.tree_utilisateurs.delete(i)
        for user in self.biblio.utilisateurs:
            self.tree_utilisateurs.insert("", "end", values=(user.username, "Oui" if user.admin else "Non", user.abonnement.type))

    def run(self):
        self.fenetre.mainloop()


if __name__ == "__main__":
    AppBibliotheque().run()
