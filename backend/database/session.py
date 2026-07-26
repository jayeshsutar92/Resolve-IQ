"""
session.py
Configures the async SQLAlchemy engine and session factory.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

# Create async engine for PostgreSQL
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Create a session factory
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db_session():
    """
    Dependency to yield an async database session.
    Automatically handles closing the session after the request.
    """
    async with AsyncSessionFactory() as session:
        yield session
