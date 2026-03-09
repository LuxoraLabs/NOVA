from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nova.utils.config import get_settings
from nova.utils.logging import get_logger
from nova.database.models import Base

logger = get_logger(__name__)

settings = get_settings()
engine = create_engine(f"sqlite:///{settings.db_path}", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    """Dependency or standard accessor for getting an SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize the database schema using SQLAlchemy."""
    logger.info("Initializing database schema...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
