import sqlite3, os, pathlib

class DBGenerator:
    __path: str

    def __init__(self, reset = True):
        self.__path = pathlib.Path('database','database.db')
        if os.path.exists(self.__path) and reset:
            os.remove(self.__path)
        os.makedirs(os.path.dirname(self.__path), exist_ok=True)

    def create(self):
        conn = sqlite3.connect(self.__path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        self.__create_beheerders(cursor)
        self.__create_toezichthouders(cursor)
        self.__create_status(cursor)
        self.__create_beperkingcategorie(cursor)
        self.__create_ervaringsdeskundigen(cursor)
        self.__create_organisaties(cursor)
        self.__create_onderzoeken(cursor)
        self.__create_deelnamen(cursor)
        self.__create_beperkingen(cursor)
        self.__create_ervaringsdeskundigen_beperkingen(cursor)
        self.__create_onderzoeken_beperkingen(cursor)
        conn.commit()
        conn.close()

    def fill(self):
        conn = sqlite3.connect(self.__path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        self.__generate_beperking_categories(cursor)
        self.__generate_beperkingen(cursor)
        self.__generate_status(cursor)
        conn.commit()
        conn.close()

    #region Create tables

    def __create_beheerders(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS beheerders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voornaam TEXT NOT NULL,
                achternaam TEXT NOT NULL,
                postcode TEXT NOT NULL,
                geslacht TEXT,
                telefoonnr TEXT NOT NULL,
                email TEXT NOT NULL,
                wachtwoord TEXT NOT NULL,
                salt TEXT NOT NULL,
                privileges INTEGER NOT NULL DEFAULT 0
            );
        """
        cursor.execute(query)

    def __create_toezichthouders(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS toezichthouders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                email TEXT NOT NULL,
                telefoonnr TEXT NOT NULL
            );
        """
        cursor.execute(query)

    def __create_status(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS status(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                beschrijving TEXT NOT NULL
            );
        """
        cursor.execute(query)
    
    def __create_beperkingcategorie(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS beperkingcategorie(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL
            );
        """
        cursor.execute(query)

    def __create_ervaringsdeskundigen(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS ervaringsdeskundigen(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voornaam TEXT NOT NULL,
                achternaam TEXT NOT NULL,
                postcode TEXT NOT NULL,
                geslacht TEXT,
                telefoonnr TEXT NOT NULL,
                email TEXT NOT NULL,
                wachtwoord TEXT NOT NULL,
                salt TEXT NOT NULL,
                geboorte_datum TEXT NOT NULL,
                gebruikte_hulpmiddelen TEXT,
                kort_voorstellen TEXT,
                bijzonderheden TEXT,
                voorwaarden INTEGER NOT NULL DEFAULT 0,
                toezichthouder_id INTEGER REFERENCES toezichthouders(id),
                voorkeur_benadering TEXT NOT NULL,
                type_onderzoek TEXT NOT NULL,
                bijzonderheden_beschikbaarheid TEXT,
                status_id INTEGER REFERENCES status(id)
            );
        """
        cursor.execute(query)

    def __create_organisaties(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS organisaties(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                type TEXT NOT NULL,
                website TEXT,
                beschrijving TEXT,
                contactpersoon TEXT NOT NULL,
                email TEXT NOT NULL,
                telefoonnr TEXT,
                overige_details TEXT,
                api_key TEXT
            );
        """
        cursor.execute(query)

    def __create_onderzoeken(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS onderzoeken(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                status_id INTEGER REFERENCES status(id),
                beschikbaar INTEGER DEFAULT 1,
                beschrijving TEXT NOT NULL DEFAULT '',
                start_datum TEXT NOT NULL,
                eind_datum TEXT NOT NULL,
                type_onderzoek TEXT NOT NULL,
                locatie TEXT,
                met_beloning INTEGER DEFAULT 0,
                beloning TEXT,
                doelgroep_leeftijd_start INTEGER NOT NULL,
                doelgroep_leeftijd_eind INTEGER NOT NULL,
                organisatie_id INTEGER REFERENCES organisaties(id)
            );
        """
        cursor.execute(query)

    def __create_deelnamen(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS deelnamen(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                datum TEXT NOT NULL,
                ervaringsdeskundige_id INTEGER REFERENCES ervaringsdeskundigen(id),
                onderzoek_id INTEGER REFERENCES onderzoeken(id),
                status_id INTEGER REFERENCES status(id)
            );
        """
        cursor.execute(query)
    
    def __create_beperkingen(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS beperkingen(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                categorie_id INTEGER REFERENCES beperkingcategorie(id)
            );
        """
        cursor.execute(query)

    def __create_ervaringsdeskundigen_beperkingen(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS ervaringsdeskundigen_beperkingen(
                ervaringsdeskundige_id INTEGER REFERENCES ervaringsdeskundigen(id),
                beperking_id INTEGER REFERENCES beperkingen(id)
            );
        """
        cursor.execute(query)

    def __create_onderzoeken_beperkingen(self, cursor: sqlite3.Cursor):
        query = """
            CREATE TABLE IF NOT EXISTS onderzoek_beperkingen(
                onderzoek_id INTEGER REFERENCES onderzoeken(id),
                beperking_id INTEGER REFERENCES beperkingen(id)
            );
        """
        cursor.execute(query)

    #endregion

    #region Fill tables (testdata)

    def __generate_beperking_categories(self, cursor: sqlite3.Cursor):
        query = """
            INSERT INTO beperkingcategorie (naam) VALUES (?);
        """

        data = [
            ["Auditieve beperkingen"],
            ["Visuele beperkingen"],
            ["Motorische / lichamelijke beperkingen"],
            ["Cognitieve / neurologische beperkingen"]
        ]

        cursor.executemany(query, data)

    def __generate_beperkingen(self, cursor: sqlite3.Cursor):
        query = """
            INSERT INTO beperkingen (naam, categorie_id) VALUES (?, ?);
        """

        data = [
            ["Doof", 1],
            ["Slechthorend", 1],
            ["Doofblind", 1],
            ["Blind", 2],
            ["Slechtziend", 2],
            ["Kleurenblind", 2],
            ["Doofblind", 2],
            ["Amputatie en mismaaktheid", 3],
            ["Artritus", 3],
            ["Fibromyalgie", 3],
            ["Reuma", 3],
            ["Verminderde handvaardigheid", 3],
            ["Spierdystrofie", 3],
            ["RSI", 3],
            ["Tremor en Spasmen", 3],
            ["Quadriplegie of tetraplegie", 3],
            ["ADHD", 4],
            ["Autisme", 4],
            ["Dyslexie", 4],
            ["Dyscalculie", 4],
            ["Leerstoornis", 4],
            ["Geheugen beperking", 4],
            ["Multiple Sclerose", 4],
            ["Epilepsie", 4],
            ["Migraine", 4]
        ]

        cursor.executemany(query, data)

    def __generate_status(self, cursor: sqlite3.Cursor):
        query = """
            INSERT INTO status (beschrijving) VALUES (?);
        """

        data = [
            ["Goedgekeurd"],
            ["Afgekeurd"],
            ["Afwachting"]
        ]

        cursor.executemany(query, data)

    #endregion

if __name__ == '__main__':
    db = DBGenerator()
    db.create()
    db.fill()