from sqlalchemy import create_engine

from config import get_database_url
from src.repository.model.base import Base


if __name__ == "__main__":
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)

        print("Dropping all existing tables...")
        Base.metadata.drop_all(engine)

        print("Creating all tables from ORM models...")
        Base.metadata.create_all(engine)

        print("✓ Database tables rebuilt successfully!")

    except Exception as e:
        print(f"✗ Failed to rebuild database tables: {e}")
        raise
