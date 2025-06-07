from sqlalchemy import inspect
from database.db_session import SessionLocal

class DBExplorerController:
    def __init__(self):
        self.db = SessionLocal()

    def list_tables(self):
        return inspect(self.db.bind).get_table_names()

    def get_columns(self, table_name):
        return inspect(self.db.bind).get_columns(table_name)

    def fetch_all(self, table_name, limit=1000):
        return self.db.execute(f"SELECT * FROM {table_name} LIMIT {limit}").fetchall()
