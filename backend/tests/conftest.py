import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.database import Base
from app.core.dependencies import get_db
from sqlalchemy.pool import NullPool

# Use the test PostgreSQL DB
TEST_DATABASE_URL = "postgresql+asyncpg://careeros:careeros@postgres:5432/careeros_test"

@pytest.fixture
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

@pytest.fixture
def testing_session_local(db_engine):
    return async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)



@pytest.fixture(autouse=True)
async def prepare_database(db_engine):
    """Create all tables in the test database before each test."""
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_db():
    """Dependency override for database session."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def db_session(testing_session_local):
    """Fixture providing a direct database session for tests."""
    async with testing_session_local() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def async_client():
    """Provide an async test client."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
