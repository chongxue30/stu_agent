from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_mysql_uri():
    return f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?charset=utf8mb4"

# Create synchronous engine
engine = create_engine(
    get_mysql_uri(),
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create synchronous session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare base class
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()