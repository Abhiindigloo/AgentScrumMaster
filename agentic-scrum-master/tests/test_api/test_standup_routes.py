import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from api.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_healthz(client: AsyncClient) -> None:
    response = await client.get("/api/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "AgentScrumMaster"


@pytest.mark.asyncio
async def test_submit_standup(client: AsyncClient) -> None:
    payload = {
        "user_id": "u1",
        "user_name": "Alice",
        "team_id": "team-test",
        "yesterday": "Built feature X",
        "today": "Test feature X",
        "blockers": None,
    }
    response = await client.post("/api/standups", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["user_id"] == "u1"


@pytest.mark.asyncio
async def test_submit_standup_with_blockers(client: AsyncClient) -> None:
    payload = {
        "user_id": "u2",
        "user_name": "Bob",
        "yesterday": "Worked on DB migration",
        "today": "Deploy to staging",
        "blockers": "Waiting for DBA approval",
    }
    response = await client.post("/api/standups", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["blocker_detected"] is True


@pytest.mark.asyncio
async def test_submit_standup_validation_error(client: AsyncClient) -> None:
    payload = {"user_id": "", "user_name": "", "yesterday": "", "today": ""}
    response = await client.post("/api/standups", json=payload)
    assert response.status_code == 422
