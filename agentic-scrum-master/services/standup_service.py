from datetime import datetime, timezone

from agents.standup_agent import StandupAgent
from agents.summary_agent import SummaryAgent
from models.standup import StandupUpdate, DailySummary
from schemas.standup import StandupUpdateRequest
from core.logging import get_logger
from core.exceptions import NotFoundError

logger = get_logger(__name__)


class StandupService:
    """Service layer for standup operations.

    Manages the lifecycle of standup updates: submission,
    storage, retrieval, and daily summary generation.
    Uses in-memory storage for Phase 1; will be replaced
    with persistent storage in a future phase.
    """

    def __init__(self) -> None:
        self._standup_agent = StandupAgent()
        self._summary_agent = SummaryAgent()
        self._updates: dict[str, StandupUpdate] = {}
        self._summaries: dict[str, DailySummary] = {}

    async def submit_update(self, request: StandupUpdateRequest) -> StandupUpdate:
        """Process and store a standup update.

        Args:
            request: Validated standup update request.

        Returns:
            Processed StandupUpdate with blocker analysis.
        """
        update = await self._standup_agent.process(request.model_dump())
        self._updates[update.id] = update

        logger.info(
            f"Standup update stored: id={update.id}, user={update.user_name}, "
            f"blockers={update.blocker_detected}"
        )
        return update

    async def get_update(self, update_id: str) -> StandupUpdate:
        """Retrieve a standup update by ID."""
        update = self._updates.get(update_id)
        if not update:
            raise NotFoundError("StandupUpdate", update_id)
        return update

    async def get_updates_by_team(
        self,
        team_id: str,
        date: str | None = None,
    ) -> list[StandupUpdate]:
        """Retrieve all standup updates for a team, optionally filtered by date."""
        updates = [u for u in self._updates.values() if u.team_id == team_id]

        if date:
            updates = [
                u for u in updates
                if u.created_at.strftime("%Y-%m-%d") == date
            ]

        updates.sort(key=lambda u: u.created_at, reverse=True)
        return updates

    async def generate_daily_summary(
        self,
        team_id: str,
        date: str | None = None,
    ) -> DailySummary:
        """Generate a daily summary for a team.

        Args:
            team_id: The team to summarize.
            date: Date string (YYYY-MM-DD). Defaults to today.

        Returns:
            DailySummary entity with aggregated data.
        """
        if not date:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        updates = await self.get_updates_by_team(team_id, date)

        summary = await self._summary_agent.process({
            "updates": updates,
            "team_id": team_id,
            "date": date,
        })

        summary_key = f"{team_id}:{date}"
        self._summaries[summary_key] = summary

        logger.info(f"Daily summary generated: team={team_id}, date={date}, updates={len(updates)}")
        return summary

    async def get_daily_summary(
        self,
        team_id: str,
        date: str | None = None,
    ) -> DailySummary:
        """Retrieve a cached daily summary."""
        if not date:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        summary_key = f"{team_id}:{date}"
        summary = self._summaries.get(summary_key)
        if not summary:
            raise NotFoundError("DailySummary", summary_key)
        return summary
