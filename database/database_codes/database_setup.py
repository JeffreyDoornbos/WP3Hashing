import sqlite3, os

db_path = '/database/sql_database/database.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Algemeen beheerders van de website
def beheerders():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS beheerders(
    beheerder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    voornaam TEXT NOT NULL,
    achternaam TEXT NOT NULL,
    postcode TEXT NOT NULL,
    geslacht TEXT NOT NULL,
    email TEXT NOT NULL,
    telefoonnummer TEXT NOT NULL
    )
    ''')

# Algemeen ervaringsdeskundigen van de website
def ervaringsdeskundigen():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ervaringsdeskundigen(
    deskundige_id INTEGER PRIMARY KEY AUTOINCREMENT,
    voornaam TEXT NOT NULL,
    achternaam TEXT NOT NULL,
    postcode TEXT NOT NULL,
    geslacht TEXT NOT NULL,
    emailadres TEXT NOT NULL UNIQUE,
    telefoonnummer TEXT NOT NULL,
    geboortedatum DATETIME NOT NULL,
    type_beperking INTEGER REFERENCES beperkingen(beperking_id),
    gebruikte_hulpmiddelen TEXT NOT NULL,
    kort_voorstellen TEXT NOT NULL,
    
    bijzonderheden TEXT,
    akkoord_voorwaarden INTEGER DEFAULT 0,
    toezichthouder INTEGER DEFAULT 0,
    
    naam_voogd_toezichthouder TEXT,
    email_voogd_toezichthouder TEXT,
    telefoonnummer_voogd_toezichthouder TEXT,
    
    voorkeur_benadering TEXT,
    type_onderzoek TEXT,
    
    bijzonderheden_beschikbaarheid TEXT,
    
    deelname_id INTEGER NOT NULL UNIQUE
    )
    ''')

# Algemeen organisaties van de website
def organisaties():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS organisaties(
    organisatie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    naam TEXT NOT NULL,
    type TEXT NOT NULL,
    website TEXT NOT NULL,
    beschrijving TEXT,
    contactpersonen TEXT NOT NULL,
    email TEXT NOT NULL,
    telefoonnummer TEXT NOT NULL,
    onderzoeks_id INTEGER NOT NULL UNIQUE
    )
    ''')

# Inlog gegevens beheerders van de website
def beheerders_inloggen():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS beheerder_inloggen(
    beheerder_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    gebruikersnaam TEXT NOT NULL UNIQUE,
    wachtwoord TEXT NOT NULL,
    beheerder_id INTEGER NOT NULL,
    admin INTEGER DEFAULT 0,
    FOREIGN KEY (beheerder_id) REFERENCES beheerders(beheerder_id)
    )
    ''')

# Inlog gegevens ervaringdeskundigen van de website
def ervaringsdeskundigen_inloggen():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ervaringsdeskundigen_inloggen(
    ervaringsdeskundige_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    gebruikersnaam TEXT NOT NULL UNIQUE,
    wachtwoord TEXT NOT NULL,
    ervaringsdeskundigen_id INTEGER NOT NULL,
    FOREIGN KEY (ervaringsdeskundigen_id) REFERENCES ervaringsdeskundigen(deskundige_id)
    )
    ''')

# Inlog gegevens organisaties van de website
def organisaties_inloggen():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS organisatie_inloggen(
    organisatie_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    gebruikersnaam TEXT NOT NULL UNIQUE,
    wachtwoord TEXT NOT NULL,
    organisatie_id INTEGER NOT NULL,
    FOREIGN KEY (organisatie_id) REFERENCES organisaties(organisatie_id)
    )
    ''')

# gegevens onderzoek
def gegevens_onderzoek():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gegevens_onderzoek(
    gegevens_id INTEGER PRIMARY KEY AUTOINCREMENT,
    titel TEXT NOT NULL,
    status INTEGER REFERENCES status(status_id),
    beschikbaar INTEGER DEFAULT 0,
    beschrijving TEXT NOT NULL,
    datum_vanaf DATE NOT NULL,
    datum_tot DATE NOT NULL,
    type_onderzoek INTEGER REFERENCES type_onderzoek(type_onderzoek_id),
    locatie TEXT NOT NULL,
    met_beloning INTEGER DEFAULT 0,
    beloning TEXT NOT NULL,
    doelgroep_leeftijd_van INTEGER,
    doelgroep_leeftijd_tot INTEGER,
    doelgroep_beperking INTEGER REFERENCES beperkingen(beperking_id),
    onderzoeks_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (onderzoeks_id) REFERENCES organisaties(onderzoeks_id)
    )
    ''')

# beperkingen
def beperkingen():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS beperkingen(
    beperking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    beperking_naam TEXT NOT NULL,
    beperking_categorie INTEGER NOT NULL,
    categorie_nummer INTEGER NOT NULL
    )
    ''')

def beperkingen_ervaringsdeskundige():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS beperkingen_ervaringsdekunsige(
    beperking_ervaringsdeskundige_id INTEGER PRIMARY KEY AUTOINCREMENT,
    deskundige_id INTEGER REFERENCES ervaringsdeskundigen(deskundige_id),
    beperking_id INTEGER REFERENCES beperkingen(beperking_id)
    )
    ''')

def beperkingen_organisatie():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS beperkingen_organisatie(
    beperking_organisatie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    organisatie_id INTEGER REFERENCES organisaties(organisatie_id),
    beperking_id INTEGER REFERENCES beperkingen(beperking_id)
    )
    ''')

# Tussen tabel met ervaringsdeskundige_id & beperking_id
# Tussen tabel met organisatie_id & beperking_id

# deelname
def deelname():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deelname(
    deelname_id INTEGER PRIMARY KEY AUTOINCREMENT,
    deelname INTEGER DEFAULT 0,
    deelname_aantal INTEGER,
    deelname_datum TEXT NOT NULL,
    ervaringsdekundigen_id INTEGER NOT NULL,
    FOREIGN KEY (ervaringsdekundigen_id) REFERENCES ervaringsdeskundigen(deskundige_id)
    )
    ''')

# Status
def status():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS status(
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_ervaringsdeskundige TEXT NOT NULL,
    status_nummer INTEGER NOT NULL
    )
    ''')

# Type onderzoek
def type_onderzoek():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS type_onderzoek(
    type_onderzoek_id INTEGER PRIMARY KEY AUTOINCREMENT,
    onderzoek_type TEXT NOT NULL,
    onderzoek_nummer INTEGER NOT NULL
    )
    ''')

# insert beperkingen
def insert_beperking(beperking_naam, beperking_categorie, categorie_nummer):
    cursor.execute('''
    INSERT OR REPLACE INTO beperkingen (beperking_naam, beperking_categorie, categorie_nummer)
    VALUES ( ?, ?, ?)
    ''', (beperking_naam, beperking_categorie, categorie_nummer))

    conn.commit()

beperking_lijst = [
    # Auditieve beperkingen
    ("Doof", "Auditieve beperkingen", 1),
    ("Slechthorend", "Auditieve beperkingen", 1),
    ("Doofblind", "Auditieve beperkingen", 1),

    # Visuele beperkingen
    ("Blind", "visuele beperkingen", 2),
    ("Slechtziend", "visuele beperkingen", 2),
    ("Kleurenblind", "visuele beperkingen", 2),
    ("Doofblind", "visuele beperkingen", 2),

    # Motorische / lichamelijke beperkingen
    ("Amputatie en mismaaktheid", "Motorische / lichamelijke beperkingen", 3),
    ("Artritus", "Motorische / lichamelijke beperkingen", 3),
    ("Fibromyalgie", "Motorische / lichamelijke beperkingen", 3),
    ("Reuma", "Motorische / lichamelijke beperkingen", 3),
    ("Verminderde handvaardigheid", "Motorische / lichamelijke beperkingen", 3),
    ("Spierdystrofie", "Motorische / lichamelijke beperkingen", 3),
    ("RSI", "Motorische / lichamelijke beperkingen", 3),
    ("Tremor en Spasmen", "Motorische / lichamelijke beperkingen", 3),
    ("Quadriplegie of tetraplegie", "Motorische / lichamelijke beperkingen", 3),

    # Cognitieve / neurologische beperkingen
    ("ADHD", "Cognitieve / neurologische beperkingen", 4),
    ("Autisme", "Cognitieve / neurologische beperkingen", 4),
    ("Dyslexie", "Cognitieve / neurologische beperkingen", 4),
    ("Dyscalculie", "Cognitieve / neurologische beperkingen", 4),
    ("Leerstoornis", "Cognitieve / neurologische beperkingen", 4),
    ("Geheugen beperking", "Cognitieve / neurologische beperkingen", 4),
    ("Multiple Sclerose", "Cognitieve / neurologische beperkingen", 4),
    ("Epilepsie", "Cognitieve / neurologische beperkingen", 4),
    ("Migraine", "Cognitieve / neurologische beperkingen", 4)
]

# Insert status
def insert_status(status_ervaringsdeskundige, status_nummer):
    cursor.execute('''
    INSERT OR REPLACE INTO status (status_ervaringsdeskundige, status_nummer)
    VALUES ( ?, ?)
    ''', (status_ervaringsdeskundige, status_nummer))

    conn.commit()

status_lijst = [
    ("Nieuw", 1),
    ("Goedgekeurd", 2),
    ("Afgekeurd", 3),
    ("Gesloten", 4)
]

# Insert type onderzoek
def insert_type_onderzoek(onderzoek_type, onderzoek_nummer):
    cursor.execute('''
    INSERT OR REPLACE INTO type_onderzoek (onderzoek_type, onderzoek_nummer)
    VALUES ( ?, ?)
    ''', (onderzoek_type, onderzoek_nummer))

    conn.commit()

type_onderzoek_lijst = [
    ("Op locatie", 1),
    ("Telefonisch", 2),
    ("Online", 3)
]

# Aanroepen tot functies
beheerders()
ervaringsdeskundigen()
organisaties()
beheerders_inloggen()
ervaringsdeskundigen_inloggen()
organisaties_inloggen()
gegevens_onderzoek()
beperkingen()
deelname()
status()
type_onderzoek()

# Insert lijsten in beperkingen, status en type_onderzoek
for beperking in beperking_lijst:
    insert_beperking(*beperking)

for staat in status_lijst:
    insert_status(*staat)

for type_onderzoek in type_onderzoek_lijst:
    insert_type_onderzoek(*type_onderzoek)

conn.commit()
conn.close()
