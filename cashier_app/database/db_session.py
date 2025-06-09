"""Database session setup using SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from cashier_app.config.settings import DB_PATH

ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = scoped_session(sessionmaker(bind=ENGINE))


def init_db() -> None:
    """Initialize database models."""
    from cashier_app.models.base import Base
    Base.metadata.create_all(bind=ENGINE)
