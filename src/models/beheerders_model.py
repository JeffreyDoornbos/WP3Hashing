import sqlite3
from pathlib import Path
from sqlite3 import Row
from .model import Model

class BeheerdersModel(Model): #Model class regelt meeste database spul, enige wat je dan nog hoeft te doen is self.query() aan te roepen
    
    def get_onderzoeken_in_afwachting(self):
        """
        Haal alle onderzoeken op met status_id = 3 (In afwachting).
        """
        query_str = """
            SELECT o.*, s.beschrijving AS status_naam
            FROM onderzoeken o
            LEFT JOIN status s ON o.status_id = s.id
            WHERE o.status_id = 3
        """
        results = self.query(query_str)
        return [dict(row) for row in results]
    
    def get_onderzoeken_afgekeurd(self):
        """
        Haal alle onderzoeken op met status_id = 2 (Afgekeurd).
        """
        query_str = """
            SELECT o.*, s.beschrijving AS status_naam
            FROM onderzoeken o
            LEFT JOIN status s ON o.status_id = s.id
            WHERE o.status_id = 2
        """
        results = self.query(query_str)
        return [dict(row) for row in results]
    
    
    def update_onderzoek_status(self, onderzoek_id, status_id):
        """
        Update de status van een onderzoek (1=Goedgekeurd, 2=Afgekeurd, 3=In afwachting).
        """
        query_str = "UPDATE onderzoeken SET status_id = ? WHERE id = ?"
        self.query(query_str, status_id, onderzoek_id)

    def get_ervaringsdeskundigen_in_afwachting(self):
        query_str = """
            SELECT e.*, s.beschrijving AS status_naam
            FROM ervaringsdeskundigen e
            LEFT JOIN status s ON e.status_id = s.id
            WHERE e.status_id = 3
        """
        results = self.query(query_str)
        return [dict(row) for row in results]

    def update_ervaringsdeskundige_status(self, ervaringsdeskundige_id, status_id):
        query_str = "UPDATE ervaringsdeskundigen SET status_id = ? WHERE id = ?"
        self.query(query_str, status_id, ervaringsdeskundige_id)
        

    def get_ervaringsdeskundigen_afgekeurd(self):
        query_str = """
            SELECT e.*, s.beschrijving AS status_naam
            FROM ervaringsdeskundigen e
            LEFT JOIN status s ON e.status_id = s.id
            WHERE e.status_id = 2
        """
        results = self.query(query_str)
        return [dict(row) for row in results]
    
    def get_deelnamen_in_afwachting(self):
        query_str = """
            SELECT d.*, s.beschrijving AS status_naam
            FROM deelnamen d
            LEFT JOIN status s ON d.status_id = s.id
            WHERE d.status_id = 3
        """
        results = self.query(query_str)
        return [dict(row) for row in results]
    
    def update_deelnamen_status(self, deelnamen_id, status_id):
        query_str = "Update deelnamen SET status_id=? WHERE id=?"
        self.query(query_str, status_id, deelnamen_id)

    def get_deelnamen_afgekeurd(self):
        query_str = """
            SELECT d.*, s.beschrijving AS status_naam
            FROM deelnamen d
            LEFT JOIN status s ON d.status_id = s.id
            WHERE d.status_id = 2
        """
        results = self.query(query_str)
        return [dict(row) for row in results]

    def create_beheerder(self, data):
        query_str = """
            INSERT INTO beheerders(voornaam, achternaam, postcode, geslacht, telefoonnr, email, wachtwoord, salt) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.query(query_str, *data, id=True)
    
    def get_beheerder_password(self, email):
        query_str = """
            SELECT id, wachtwoord FROM beheerders WHERE email = ?
        """
        return self.query(query_str, email, first=True)
    
    def get_row_count_for(self, table:str, status:int)->int:
        query_str = f"""
            SELECT id FROM {table} WHERE status_id=?
        """
        rows = self.query(query_str, status)
        if not rows:
            return 0
        return len(rows)