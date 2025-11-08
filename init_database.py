import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from src.database import DATABASE_URL
from src.repository.model.base import Base
from src.repository.model.file import File
from src.repository.model.user import User
from src.service.supabase_storage_service import SupabaseStorageService


async def run_migration():
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        print("Dropping all existing tables...")
        await conn.run_sync(Base.metadata.drop_all)

        print("Creating all tables from ORM models...")
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("✓ Database tables rebuilt successfully!")


async def clear_bucket():
    print("Clearing storage bucket...")
    storage_service = SupabaseStorageService()
    await storage_service.clear_bucket()
    print("✓ Storage bucket cleared")


async def init_database():
    await run_migration()
    await clear_bucket()


if __name__ == "__main__":
    try:
        asyncio.run(init_database())
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        raise
