"""
Database engine and session factory for the HSATracker backend.

Uses SQLAlchemy's async engine with the asyncpg driver so all DB I/O is
non-blocking and compatible with FastAPI's async request handlers.
"""

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://hsatracker:changeme@localhost:5432/hsatracker",
)

# echo=False keeps SQL queries out of logs in production.
# Set to True temporarily when debugging query behaviour.
engine = create_async_engine(DATABASE_URL, echo=False)

# expire_on_commit=False prevents SQLAlchemy from expiring ORM objects after
# commit, which would trigger lazy-load errors in an async context.
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a scoped async DB session per request.

    Usage:
        async def my_endpoint(db: AsyncSession = Depends(get_db)): ...

    The session is automatically closed when the request finishes, whether it
    succeeds or raises an exception.
    """
    async with AsyncSessionLocal() as session:
        yield session
