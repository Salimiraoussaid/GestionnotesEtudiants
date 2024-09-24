from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

class NoteApp(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestion des Notes des Étudiants')

        # Stylesheet pour la fenêtre principale
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;  /* Couleur de fond */
                font-family: Arial, sans-serif;  /* Police de caractère */
            }
        """)

        # Layout principal
        layout = QVBoxLayout()

        # Champs de saisie
        self.nomInput = QLineEdit()
        self.nomInput.setPlaceholderText('Nom')
        self.nomInput.setStyleSheet("QLineEdit { padding: 10px; border: 1px solid #ccc; border-radius: 5px; }")

        self.prenomInput = QLineEdit()
        self.prenomInput.setPlaceholderText('Prénom')
        self.prenomInput.setStyleSheet("QLineEdit { padding: 10px; border: 1px solid #ccc; border-radius: 5px; }")

        self.noteInput = QLineEdit()
        self.noteInput.setPlaceholderText('Note')
        self.noteInput.setStyleSheet("QLineEdit { padding: 10px; border: 1px solid #ccc; border-radius: 5px; }")

        # Boutons
        self.addButton = QPushButton('Ajouter')
        self.updateButton = QPushButton('Modifier')
        self.deleteButton = QPushButton('Supprimer')
        self.loadButton = QPushButton('Charger')

        # Styles pour les boutons
        buttons_style = """
            QPushButton {
                background-color: #007BFF; /* Couleur de fond */
                color: white; /* Couleur du texte */
                border: none; /* Pas de bordure */
                padding: 10px 15px; /* Espacement */
                border-radius: 5px; /* Coins arrondis */
            }
            QPushButton:hover {
                background-color: #0056b3; /* Couleur au survol */
            }
        """
        self.addButton.setStyleSheet(buttons_style)
        self.updateButton.setStyleSheet(buttons_style)
        self.deleteButton.setStyleSheet(buttons_style)
        self.loadButton.setStyleSheet(buttons_style)

        # Table pour afficher les notes
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # 4 colonnes pour ID, Nom, Prénom et Note
        self.table.setHorizontalHeaderLabels(['ID', 'Nom', 'Prénom', 'Note'])
        self.table.setColumnHidden(0, True)  # Masquer la colonne ID
        # Ajout des widgets au layout
        formLayout = QHBoxLayout()
        formLayout.addWidget(self.nomInput)
        formLayout.addWidget(self.prenomInput)
        formLayout.addWidget(self.noteInput)

        layout.addLayout(formLayout)
        layout.addWidget(self.addButton)
        layout.addWidget(self.updateButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Connexion des boutons aux fonctions
        self.addButton.clicked.connect(self.ajouter)
        self.updateButton.clicked.connect(self.modifier)
        self.deleteButton.clicked.connect(self.supprimer)
        self.loadButton.clicked.connect(self.chargerNote)
        self.table.cellClicked.connect(self.on_row_selected)

        self.chargerNote()

    def ajouter(self):
        nom = self.nomInput.text()
        prenom = self.prenomInput.text()
        note = self.noteInput.text()

        if nom and prenom and note:
            self.db.ajouter(nom, prenom, note)
            self.chargerNote()
            self.nomInput.clear()
            self.prenomInput.clear()
            self.noteInput.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis')

    def modifier(self):
        selected_row = self.table.currentRow()  # Récupérer la ligne sélectionnée
        if selected_row == -1:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une note à modifier.')
            return

        # Récupérer l'ID de la note (note_id se trouve à la position 0 de la table)
        note_id = int(self.table.item(selected_row, 0).text())

        # Récupérer les nouvelles informations à partir des champs de saisie
        nom = self.nomInput.text()
        prenom = self.prenomInput.text()
        note = self.noteInput.text()

        if nom and prenom and note.isdigit():
            # Utiliser self.db.update_note avec les données obtenues
            self.db.modifier(note_id, nom, prenom, int(note))
            self.chargerNote()
            self.nomInput.clear()
            self.prenomInput.clear()
            self.noteInput.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez entrer des informations valides.')

    def on_row_selected(self, row, column):
        # Récupérer les informations de la ligne sélectionnée
        nom = self.table.item(row, 1).text()
        prenom = self.table.item(row, 2).text()
        note = self.table.item(row, 3).text()

        # Remplir les champs de saisie avec les informations de la ligne
        self.nomInput.setText(nom)
        self.prenomInput.setText(prenom)
        self.noteInput.setText(note)

    def supprimer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            note_id = int(self.table.item(selected_row, 0).text())
            self.db.supprimer(note_id)
            self.chargerNote()
            self.nomInput.clear()
            self.prenomInput.clear()
            self.noteInput.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une note à supprimer.')

    def chargerNote(self):
        notes = self.db.AfficherLesNotes()
        self.table.setRowCount(len(notes))

        for row_index, row in enumerate(notes):
            for col_index, data in enumerate(row):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(data)))
