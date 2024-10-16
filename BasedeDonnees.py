import sqlite3

class Database:
    def __init__(self, db_name='notes_etudiants.db'):
        self.nomBaseDonnee = db_name
        self.creerTable()

    def creerTable(self):
        conn = sqlite3.connect(self.nomBaseDonnee)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            note INTEGER NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

    def ajouter(self, nom, prenom, note):
        conn = sqlite3.connect(self.nomBaseDonnee)
        c = conn.cursor()
        c.execute('INSERT INTO notes (nom, prenom, note) VALUES (?, ?, ?)', (nom, prenom, note))
        conn.commit()
        conn.close()

    def modifier(self, id, nom, prenom, note):
        conn = sqlite3.connect(self.nomBaseDonnee)
        c = conn.cursor()
        c.execute('UPDATE notes SET nom = ?, prenom = ?, note = ? WHERE id = ?', (nom, prenom, note, id))
        conn.commit()
        conn.close()

    def supprimer(self, id):
        conn = sqlite3.connect(self.nomBaseDonnee)
        c = conn.cursor()
        c.execute('DELETE FROM notes WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def AfficherLesNotes(self):
        conn = sqlite3.connect(self.nomBaseDonnee)
        c = conn.cursor()
        c.execute('SELECT * FROM notes')
        rows = c.fetchall()
        conn.close()
        return rows
