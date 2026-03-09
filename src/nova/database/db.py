from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from nova.utils.config import get_settings
from nova.utils.logging import get_logger
from nova.database.models import Base

logger = get_logger(__name__)

settings = get_settings()
engine = create_engine(f"sqlite:///{settings.db_path}", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def _migrate_is_setup_completed() -> None:
    """Add is_setup_completed column if missing and backfill existing users."""
    with engine.connect() as conn:
        cursor = conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in cursor.fetchall()]
        if "is_setup_completed" in columns:
            logger.debug("Column is_setup_completed already exists")
            return

        logger.info("Adding is_setup_completed column to users table")
        conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN is_setup_completed INTEGER NOT NULL DEFAULT 0"
            )
        )
        conn.commit()

        # Backfill: set True where all required fields are filled
        conn.execute(
            text("""
                UPDATE users SET is_setup_completed = 1
                WHERE name IS NOT NULL AND TRIM(name) != ''
                AND weight IS NOT NULL
                AND height IS NOT NULL
                AND google_sheet_url IS NOT NULL AND TRIM(google_sheet_url) != ''
            """)
        )
        conn.commit()
        logger.info("Backfilled is_setup_completed for existing users")


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
        _migrate_is_setup_completed()
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
