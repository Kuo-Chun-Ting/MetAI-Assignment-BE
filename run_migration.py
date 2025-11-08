import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from config import get_database_url
from src.repository.model.base import Base
from src.repository.model.file import File
from src.repository.model.user import User


async def run_migration():
    engine = create_async_engine(get_database_url())

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
