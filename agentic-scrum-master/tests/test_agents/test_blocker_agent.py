import pytest
from agents.blocker_agent import BlockerAgent


@pytest.fixture
def agent() -> BlockerAgent:
    return BlockerAgent()


@pytest.mark.asyncio
async def test_explicit_blocker_detected(agent: BlockerAgent) -> None:
    data = {
        "user_id": "u1",
        "yesterday": "Worked on auth module",
        "today": "Continue auth",
        "blockers": "Waiting for API keys from DevOps team",
    }
    result = await agent.process(data)
    assert result["blocker_detected"] is True
    assert len(result["blocker_details"]) > 0


@pytest.mark.asyncio
async def test_no_blocker(agent: BlockerAgent) -> None:
    data = {
        "user_id": "u2",
        "yesterday": "Completed frontend design",
        "today": "Start integration tests",
        "blockers": None,
    }
    result = await agent.process(data)
    assert result["blocker_detected"] is False
    assert result["blocker_details"] == []


@pytest.mark.asyncio
async def test_implicit_blocker_in_today(agent: BlockerAgent) -> None:
    data = {
        "user_id": "u3",
        "yesterday": "Worked on database migration",
        "today": "Stuck on the deployment pipeline config",
        "blockers": None,
    }
    result = await agent.process(data)
    assert result["blocker_detected"] is True
    assert len(result["blocker_details"]) > 0


@pytest.mark.asyncio
async def test_multiple_explicit_blockers(agent: BlockerAgent) -> None:
    data = {
        "user_id": "u4",
        "yesterday": "Code review",
        "today": "Fix bugs",
        "blockers": "- No access to staging DB\n- Waiting for design approval",
    }
    result = await agent.process(data)
    assert result["blocker_detected"] is True
    assert len(result["blocker_details"]) == 2


@pytest.mark.asyncio
async def test_empty_blocker_field(agent: BlockerAgent) -> None:
    data = {
        "user_id": "u5",
        "yesterday": "Deployed v2",
        "today": "Monitor dashboards",
        "blockers": "",
    }
    result = await agent.process(data)
    assert result["blocker_detected"] is False
