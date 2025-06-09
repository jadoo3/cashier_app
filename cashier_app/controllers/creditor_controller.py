"""Controller for creditor management."""

from sqlalchemy.orm import Session

from cashier_app.models.creditor import Creditor


class CreditorController:
    """Manage creditor CRUD operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_creditor(self, name: str, phone: str | None = None) -> Creditor:
        creditor = Creditor(name=name, phone=phone)
        self.db.add(creditor)
        self.db.commit()
        return creditor

    def list_creditors(self) -> list[Creditor]:
        return self.db.query(Creditor).all()
