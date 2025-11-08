import asyncio
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import create_async_engine

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from src.repository.model.base import Base
from src.repository.model.file import File
from src.repository.model.user import User


async def run_migration():
    database_url = f"postgresql+asyncpg://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_async_engine(database_url)

    async with engine.begin() as conn:
        print("Dropping all existing tables...")
        await conn.run_sync(Base.metadata.drop_all)

        print("Creating all tables from ORM models...")
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("✓ Database tables rebuilt successfully!")


if __name__ == "__main__":
    try:
        asyncio.run(run_migration())
    except Exception as e:
        print(f"✗ Failed to rebuild database tables: {e}")
        raise
