from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine with connection pooling and fail-safe configuration
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # checks connection health before executing query
    pool_size=5,         # standard pool size
    max_overflow=10,     # max overflow connections
    echo=False           # set True in local dev debugging if needed
)

# Standard session factory for non-async DB operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    FastAPI dependency that provides a transactional database session.
    Automatically closes the session at the end of the request cycle.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
