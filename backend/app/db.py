import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy import select, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/farmdb")

# Create engine with connection pool settings that handle failures gracefully
engine = create_async_engine(
    DATABASE_URL, 
    future=True, 
    echo=False,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,    # Recycle connections after 1 hour
    connect_args={
        "server_settings": {
            "application_name": "farmassist"
        }
    }
)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency for FastAPI endpoints if needed
async def get_db():
    """
    Database dependency that gracefully handles connection errors.
    Returns a session if available, or None if database is unavailable.
    """
    session = None
    try:
        session = AsyncSessionLocal()
        # Test connection with a simple query
        await session.execute(text("SELECT 1"))
        yield session
    except (OperationalError, ConnectionRefusedError, Exception) as e:
        print(f"Database connection error in get_db: {e}")
        print("Database may not be running. Endpoints will return empty/default responses.")
        # Close session if it was partially created
        if session:
            try:
                await session.close()
            except:
                pass
        yield None
    finally:
        # Ensure session is properly closed
        if session:
            try:
                await session.close()
            except:
                pass
