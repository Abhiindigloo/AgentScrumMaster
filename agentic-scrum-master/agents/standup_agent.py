from typing import Any
from datetime import datetime, timezone

from agents.base_agent import BaseAgent
from agents.blocker_agent import BlockerAgent
from models.standup import StandupUpdate


class StandupAgent(BaseAgent):
    """Agent responsible for processing standup updates.

    Coordinates the standup update flow: validates input,
    runs blocker detection, and produces a processed StandupUpdate entity.
    """

    def __init__(self) -> None:
        super().__init__(name="standup_processor")
        self._blocker_agent = BlockerAgent()

    async def process(self, data: dict[str, Any]) -> StandupUpdate:
        """Process a raw standup update through the agent pipeline.

        Args:
            data: Dict containing standup fields (user_id, yesterday, today, blockers, etc.)

        Returns:
            Fully processed StandupUpdate entity with blocker analysis.
        """
        self._log_start(f"user={data.get('user_id', 'unknown')}")

        blocker_result = await self._blocker_agent.process(data)

        update = StandupUpdate(
            user_id=data["user_id"],
            user_name=data["user_name"],
            team_id=data.get("team_id", "default"),
            sprint_id=data.get("sprint_id"),
            yesterday=data["yesterday"],
            today=data["today"],
            blockers=data.get("blockers"),
            blocker_detected=blocker_result["blocker_detected"],
            blocker_details=blocker_result["blocker_details"],
            created_at=datetime.now(timezone.utc),
        )

        self._log_complete(f"id={update.id}, blockers={update.blocker_detected}")
        return update
