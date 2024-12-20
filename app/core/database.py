from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings

DATABASE_URL = settings.ASYNC_POSTGRES_URL

engine = create_async_engine(DATABASE_URL)

# Async database session setup
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# Dependency to get the database session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
