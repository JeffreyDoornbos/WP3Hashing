from sqlite3 import connect, Connection, Row
from pathlib import Path

class Model:
    @property
    def path_to_database(self):
        path_to_file = Path(__file__).resolve()
        project_root = path_to_file.parent.parent.parent
        db_path = project_root / "database" / "database.db"
        print(f"[DEBUG] Database gebruikt door Model: {db_path}")
        return db_path
    
    def query(self, query: str, *args, many=False, first=False, id=False):
        conn = self.__open_connection()
        cursor = conn.cursor()
        if many:
            cursor.executemany(query, args)
        else:
            cursor.execute(query, args)
        conn.commit()
        result = None
        if first:
            result = cursor.fetchone()
        elif id:
            result = cursor.lastrowid 
        else:
            result = cursor.fetchall()
        conn.close()
        return result

    def __open_connection(self) -> Connection:
        conn = connect(self.path_to_database)
        conn.row_factory = Row
        return conn

    def connect(self) -> Connection:
        return self.__open_connection()