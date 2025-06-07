from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging

# إعداد التسجيل
logger = logging.getLogger(__name__)

# إنشاء قاعدة البيانات
SQLALCHEMY_DATABASE_URL = "sqlite:///./cashier.db"

# إنشاء محرك قاعدة البيانات
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# إنشاء جلسة قاعدة البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء قاعدة للـ models
Base = declarative_base()

@contextmanager
def session_scope():
    """مدير سياق للتعامل مع جلسات قاعدة البيانات"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {str(e)}", exc_info=True)
        raise
    finally:
        session.close()

def init_db():
    """تهيئة قاعدة البيانات"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        raise
