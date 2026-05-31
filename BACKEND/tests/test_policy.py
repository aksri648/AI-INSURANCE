import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import async_session, Base, engine
from app.models import User, Policy, Benefit
from sqlalchemy import select
import uuid


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user():
    async with async_session() as session:
        user = User(clerk_id="test_clerk_123", email="test@example.com", name="Test User")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest.mark.asyncio
async def test_create_policy(test_user):
    async with async_session() as session:
        policy = Policy(
            user_id=test_user.id,
            title="Test Health Policy",
            insurer="Test Insurer",
            policy_type="health",
            status="analyzed",
        )
        session.add(policy)
        await session.commit()
        await session.refresh(policy)

        assert policy.title == "Test Health Policy"
        assert policy.policy_type == "health"
        assert policy.status == "analyzed"


@pytest.mark.asyncio
async def test_create_benefit(test_user):
    async with async_session() as session:
        policy = Policy(user_id=test_user.id, title="Test Policy", policy_type="health")
        session.add(policy)
        await session.flush()

        benefit = Benefit(
            policy_id=policy.id,
            name="Hospitalization Cover",
            coverage_amount="₹5,00,000",
            waiting_period="30 days",
        )
        session.add(benefit)
        await session.commit()

        result = await session.execute(
            select(Benefit).where(Benefit.policy_id == policy.id)
        )
        benefits = result.scalars().all()
        assert len(benefits) == 1
        assert benefits[0].name == "Hospitalization Cover"


@pytest.mark.asyncio
async def test_policy_summary(test_user):
    async with async_session() as session:
        policy = Policy(
            user_id=test_user.id,
            title="Life Insurance Policy",
            policy_type="life",
            status="analyzed",
            summary="A comprehensive life insurance policy with death benefit and critical illness cover.",
        )
        session.add(policy)
        await session.commit()
        await session.refresh(policy)

        assert policy.summary is not None
        assert "life insurance" in policy.summary.lower()


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
