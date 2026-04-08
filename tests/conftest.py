import pytest
import os
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Set environment string before importing app modules
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["ADMIN_TOKEN"] = "test-token"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["ENVIRONMENT"] = "testing"

from app.main import app
from app.database import get_db, Base

engine_test = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
AsyncSessionLocalTest = async_sessionmaker(engine_test, expire_on_commit=False)

async def override_get_db():
    async with AsyncSessionLocalTest() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def create_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture
def admin_headers():
    return {"Authorization": "Bearer test-token"}
