from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

class NoteApp(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestion des Notes des Étudiants')
        self.setWindowIcon(QIcon('icons/app_icon.png'))  # Assurez-vous d'avoir une icône appropriée

        # Stylesheet global
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;  /* Couleur de fond sombre */
                color: #D8DEE9;  /* Couleur du texte claire */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #4C566A;
                border-radius: 8px;
                background-color: #3B4252;
                color: #D8DEE9;
            }
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QTableWidget {
                background-color: #3B4252;
                border: none;
                gridline-color: #4C566A;
                color: #D8DEE9;
            }
            QHeaderView::section {
                background-color: #4C566A;
                color: #ECEFF4;
                padding: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #81A1C1;
                color: #2E3440;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Titre
        title = QLabel("Gestion des Notes des Étudiants")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont('Segoe UI', 16, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #81A1C1;")
        main_layout.addWidget(title)

        # Champs de saisie
        form_layout = QHBoxLayout()
        form_layout.setSpacing(10)

        self.nomInput = QLineEdit()
        self.nomInput.setPlaceholderText('Nom')
        self.nomInput.setFixedHeight(40)
        form_layout.addWidget(self.nomInput)

        self.prenomInput = QLineEdit()
        self.prenomInput.setPlaceholderText('Prénom')
        self.prenomInput.setFixedHeight(40)
        form_layout.addWidget(self.prenomInput)

        self.noteInput = QLineEdit()
        self.noteInput.setPlaceholderText('Note')
        self.noteInput.setFixedHeight(40)
        self.noteInput.setValidator(QtGui.QIntValidator(0, 100))  # Valider uniquement les nombres entre 0 et 100
        form_layout.addWidget(self.noteInput)

        main_layout.addLayout(form_layout)

        # Boutons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.addButton = QPushButton('Ajouter')
        self.addButton.setIcon(QIcon('icons/add.png'))  # Assurez-vous d'avoir les icônes appropriées
        button_layout.addWidget(self.addButton)

        self.updateButton = QPushButton('Modifier')
        self.updateButton.setIcon(QIcon('icons/edit.png'))
        button_layout.addWidget(self.updateButton)

        self.deleteButton = QPushButton('Supprimer')
        self.deleteButton.setIcon(QIcon('icons/delete.png'))
        button_layout.addWidget(self.deleteButton)

        self.loadButton = QPushButton('Charger')
        self.loadButton.setIcon(QIcon('icons/load.png'))
        button_layout.addWidget(self.loadButton)

        main_layout.addLayout(button_layout)

        # Table pour afficher les notes
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # ID, Nom, Prénom, Note
        self.table.setHorizontalHeaderLabels(['ID', 'Nom', 'Prénom', 'Note'])
        self.table.setColumnHidden(0, True)  # Masquer la colonne ID
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        # Connexion des boutons aux fonctions
        self.addButton.clicked.connect(self.ajouter)
        self.updateButton.clicked.connect(self.modifier)
        self.deleteButton.clicked.connect(self.supprimer)
        self.loadButton.clicked.connect(self.chargerNote)
        self.table.cellClicked.connect(self.on_row_selected)

        self.chargerNote()

    def ajouter(self):
        nom = self.nomInput.text().strip()
        prenom = self.prenomInput.text().strip()
        note = self.noteInput.text().strip()

        if nom and prenom and note:
            if not note.isdigit() or not (0 <= int(note) <= 100):
                QMessageBox.warning(self, 'Erreur', 'Veuillez entrer une note valide entre 0 et 100.')
                return

            self.db.ajouter(nom, prenom, int(note))
            self.chargerNote()
            self.nomInput.clear()
            self.prenomInput.clear()
            self.noteInput.clear()
            QMessageBox.information(self, 'Succès', 'Note ajoutée avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')

    def modifier(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une note à modifier.')
            return

        note_id = int(self.table.item(selected_row, 0).text())
        nom = self.nomInput.text().strip()
        prenom = self.prenomInput.text().strip()
        note = self.noteInput.text().strip()

        if nom and prenom and note:
            if not note.isdigit() or not (0 <= int(note) <= 100):
                QMessageBox.warning(self, 'Erreur', 'Veuillez entrer une note valide entre 0 et 100.')
                return

            self.db.modifier(note_id, nom, prenom, int(note))
            self.chargerNote()
            self.nomInput.clear()
            self.prenomInput.clear()
            self.noteInput.clear()
            QMessageBox.information(self, 'Succès', 'Note modifiée avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')

    def supprimer(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            note_id = int(self.table.item(selected_row, 0).text())
            confirmation = QMessageBox.question(
                self, 'Confirmer Suppression',
                'Êtes-vous sûr de vouloir supprimer cette note ?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirmation == QMessageBox.StandardButton.Yes:
                self.db.supprimer(note_id)
                self.chargerNote()
                self.nomInput.clear()
                self.prenomInput.clear()
                self.noteInput.clear()
                QMessageBox.information(self, 'Succès', 'Note supprimée avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une note à supprimer.')

    def on_row_selected(self, row, column):
        nom = self.table.item(row, 1).text()
        prenom = self.table.item(row, 2).text()
        note = self.table.item(row, 3).text()

        self.nomInput.setText(nom)
        self.prenomInput.setText(prenom)
        self.noteInput.setText(note)

    def chargerNote(self):
        notes = self.db.AfficherLesNotes()
        self.table.setRowCount(len(notes))

        for row_index, row in enumerate(notes):
            for col_index, data in enumerate(row):
                item = QTableWidgetItem(str(data))
                if col_index == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.resizeRowsToContents()

