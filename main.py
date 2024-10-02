import sys

from PyQt6.QtWidgets import QApplication

from BasedeDonnees import Database
from fenetre import NoteApp

app = QApplication([])

# Instanciation de la base de données
db = Database()

# Création de l'interface utilisateur
fen = NoteApp(db)
fen.show()

#sys.exit(app.exec())
app.exec()