"""Common mixins used across models."""

from datetime import datetime
from sqlalchemy import Column, DateTime


class TimestampMixin:
    """Adds created_at and updated_at timestamp columns."""

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
