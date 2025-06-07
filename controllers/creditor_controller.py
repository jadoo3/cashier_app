from sqlalchemy.exc import IntegrityError
from database.db_session import SessionLocal
from models.creditor import Creditor

class CreditorController:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, name, balance=0.0, notes=None):
        c = Creditor(name=name, balance=balance, notes=notes)
        self.db.add(c)
        try:
            self.db.commit()
            self.db.refresh(c)
            return c
        except IntegrityError:
            self.db.rollback()
            raise

    def list_all(self):
        return self.db.query(Creditor).all()

    def get(self, creditor_id):
        return self.db.query(Creditor).get(creditor_id)

    def update_balance(self, creditor_id, amount):
        c = self.get(creditor_id)
        if c:
            c.balance += amount
            self.db.commit()
            self.db.refresh(c)
        return c
