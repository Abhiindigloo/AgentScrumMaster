import pytest
from services.standup_service import StandupService
from schemas.standup import StandupUpdateRequest


@pytest.fixture
def service() -> StandupService:
    return StandupService()


@pytest.mark.asyncio
async def test_submit_and_retrieve(service: StandupService) -> None:
    request = StandupUpdateRequest(
        user_id="u1",
        user_name="Alice",
        team_id="team-a",
        yesterday="Built login page",
        today="Add password reset",
        blockers=None,
    )
    update = await service.submit_update(request)
    assert update.user_id == "u1"
    assert update.user_name == "Alice"

    retrieved = await service.get_update(update.id)
    assert retrieved.id == update.id


@pytest.mark.asyncio
async def test_list_by_team(service: StandupService) -> None:
    for name, team in [("Alice", "team-a"), ("Bob", "team-a"), ("Charlie", "team-b")]:
        await service.submit_update(StandupUpdateRequest(
            user_id=name.lower(),
            user_name=name,
            team_id=team,
            yesterday="Did work",
            today="More work",
        ))

    team_a = await service.get_updates_by_team("team-a")
    assert len(team_a) == 2

    team_b = await service.get_updates_by_team("team-b")
    assert len(team_b) == 1


@pytest.mark.asyncio
async def test_generate_summary(service: StandupService) -> None:
    await service.submit_update(StandupUpdateRequest(
        user_id="u1",
        user_name="Alice",
        team_id="team-a",
        yesterday="Finished API",
        today="Start tests",
        blockers="Blocked by missing test data",
    ))
    await service.submit_update(StandupUpdateRequest(
        user_id="u2",
        user_name="Bob",
        team_id="team-a",
        yesterday="Code review",
        today="Deploy staging",
    ))

    summary = await service.generate_daily_summary("team-a")
    assert summary.total_updates == 2
    assert summary.blockers_detected >= 1
    assert "Alice" in summary.members_reported
    assert "Bob" in summary.members_reported
