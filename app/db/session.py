from typing import AsyncGenerator, Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

engine_url = URL.create(
    "mysql+aiomysql",
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_HOST,
    database=settings.DATABASE_NAME,
    query={"charset": "utf8mb4"}
)

engine = create_async_engine(
    url=engine_url,
    echo=True,
    pool_size=10,
    pool_timeout=30,
    pool_recycle=1800,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as session:
        yield session
