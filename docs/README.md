Bibliothèque Python


Auteur

Projet réalisé par Maxence.


Une application de gestion de bibliothèque en Python avec interface graphique Tkinter.
Elle permet de gérer des utilisateurs, des livres (papier et numériques), et les emprunts.


Fonctionnalités

Gestion des utilisateurs (ajout, rôle admin ou utilisateur classique)

Gestion des livres (ajout, recherche par titre ou auteur)

Emprunt et retour de livres par les utilisateurs

Historique des emprunts pour chaque utilisateur

Sauvegarde et chargement du catalogue en JSON

Export du catalogue en CSV

Interface graphique simple avec Tkinter


Structure du projet

mon_projet/
├─ src/
│  ├─ models.py          # Classes Livre, LivreNumerique, Utilisateur, Bibliotheque
│  ├─ file_manager.py    # Gestion JSON et CSV
│  ├─ interface.py       # Interface Tkinter
│  └─ exceptions.py      # Exceptions personnalisées
├─ data/                 # Dossier pour le JSON et CSV
├─ main.py               # Point d’entrée de l’application
├─tests/                 # tests pytest
└─ README.md


Utilisation

Lancer l’application :
python main.py

L’application crée un catalogue initial et sauvegarde les utilisateurs et livres dans data/catalogue.json.

Les utilisateurs peuvent emprunter et rendre des livres. L’historique est conservé entre les sessions.

Le catalogue peut également être exporté en CSV (data/catalogue.csv).







Prérequis

Avant de lancer l’application, assure-toi d’avoir :


Environnement

Python 3.9 ou supérieur

Un système compatible : Windows, macOS ou Linux


Modules Python nécessaires

Les modules utilisés sont tous standards sauf Pytest (pour les tests) :

Tkinter (intégré par défaut avec Python sur Windows/macOS)

→ Sur Linux, il peut nécessiter une installation :
sudo apt install python3-tk


json (inclus dans Python)

os (inclus dans Python)

pytest (uniquement pour exécuter les tests)

Installation :
pip install pytest
