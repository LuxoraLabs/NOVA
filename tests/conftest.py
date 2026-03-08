import os

# We must set this before importing anything that imports get_settings
os.environ["TELEGRAM_BOT_TOKEN"] = "test_telegram_token"
os.environ["OPENAI_API_KEY"] = "test_openai_key"

import pytest
from unittest import mock
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from nova.database.models import Base


@pytest.fixture(autouse=True)
def mock_env():
    """Mock environment variables for all tests."""
    with mock.patch.dict(
        os.environ,
        {
            "TELEGRAM_BOT_TOKEN": "test_telegram_token",
            "OPENAI_API_KEY": "test_openai_key",
        },
        clear=False,
    ):
        yield


@pytest.fixture
def mock_db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # We patch the SessionLocal class inside nova.database.repository
    # to return a session connected to our in-memory DB.
    with mock.patch("nova.database.repository.SessionLocal", SessionLocal):
        db = SessionLocal()
        yield db
        db.close()
        Base.metadata.drop_all(bind=engine)
