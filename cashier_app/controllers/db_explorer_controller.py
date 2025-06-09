"""Controller for raw database queries."""

from sqlalchemy.orm import Session
from sqlalchemy import text


class DBExplorerController:
    """Allows executing simple raw SQL queries."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_table(self, table_name: str, limit: int = 1000) -> list[dict]:
        result = self.db.execute(text(f"SELECT * FROM {table_name} LIMIT :limit"), {"limit": limit})
        return [dict(row) for row in result]
