import sqlite3


class databaseConnection():
    """Class for talking to database. This class provides the following
    functions:
        - __init__()
        - commit()
        - initDb()
        - close()
        - newNote(title, body)
        - updateNote(id, title, body)
        - deleteNote(id)
        - newLabel(name)
        - updateLabel(id, name)
        - deleteLabel(id)
        - labelNote(noteid, labelid)
        - unlabelNote(noteid, labelid)
    Functions with New* return the id of the newly created entry in DB."""

    def __init__(self, dbname):
        """Initialize connection with the database."""
        self.dbconn = sqlite3.connect(dbname)
        self.c = self.dbconn.cursor()

    def commit(self):
        self.dbconn.commit()

    def initDb(self):
        self.c.execute('CREATE TABLE notes ('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'title TEXT,'
                       'body TEXT)')
        self.c.execute('CREATE TABLE labels ('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'name TEXT)')
        self.c.execute('CREATE TABLE noteslabels (note int, label int)')
        self.commit()

    def close(self):
        self.dbconn.close()

    # Commands for note management.
    def newNote(self, title, body):
        self.c.execute('INSERT INTO notes (title, body) VALUES (?, ?)',
                       (title, body))
        self.commit()
        return self.c.lastrowid

    def updateNote(self, id, title, body):
        self.c.execute('UPDATE notes SET title = ?, body = ? WHERE id = ?',
                       (title, body, id))
        self.commit()

    def deleteNote(self, id):
        self.c.execute('DELETE FROM notes WHERE id = ?', id)
        self.c.execute('DELETE FROM noteslabels WHERE note = ?', id)
        self.commit()

    # Commands for label management.
    def newLabel(self, name):
        self.c.execute('INSERT INTO labels (name) VALUES (?)', (name,))
        self.commit()
        return self.c.lastrowid

    def updateLabel(self, id, name):
        self.c.execute('UPDATE labels SET name = ? WHERE id = ?', (name, id))
        self.commit()

    def deleteLabel(self, id):
        self.c.execute('DELETE FROM labels WHERE id = ?', id)
        self.c.execute('DELETE FROM noteslabels WHERE labelid = ?', id)
        self.commit()

    # Commands for labeling notes.
    def labelNote(self, noteid, labelid):
        self.c.execute('INSERT INTO noteslabels (note, label) VALUES (?, ?)',
                       (noteid, labelid))
        self.commit()

    def unlabelNote(self, noteid, labelid):
        self.c.execute('DELETE FROM noteslabels WHERE '
                       'note = ? AND label = ?', (noteid, labelid))
        self.commit()
