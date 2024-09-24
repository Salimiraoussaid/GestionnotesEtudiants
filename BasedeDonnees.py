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

    # Styles pour la table
    self.table.setStyleSheet("""
        QTableWidget {
            border: 1px solid #ccc; /* Bordure de la table */
            border-radius: 5px; /* Coins arrondis */
            background-color: white; /* Couleur de fond de la table */
        }
        QHeaderView::section {
            background-color: #007BFF; /* Couleur d'arrière-plan des en-têtes */
            color: white; /* Couleur du texte des en-têtes */
            padding: 10px; /* Espacement des en-têtes */
        }
        QTableWidget::item {
            padding: 10px; /* Espacement des éléments de la table */
        }
    """)

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
