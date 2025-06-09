from sqlalchemy import Column, Integer, String, DateTime, JSON
from models.base import Base, TimestampMixin

class AuditLog(TimestampMixin, Base):
    """نموذج لتسجيل التغييرات في النظام"""
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String, nullable=False)  # نوع الكيان (مثل: Product, Sale, Creditor)
    entity_id = Column(Integer, nullable=False)  # معرف الكيان
    action = Column(String, nullable=False)  # نوع العملية (مثل: created, updated, deleted)
    details = Column(String)  # تفاصيل إضافية عن العملية
    changes = Column(JSON)  # التغييرات التي تمت (قيم قبل وبعد)

    def __repr__(self):
        return f"<AuditLog {self.entity} {self.action} {self.entity_id}>" 

