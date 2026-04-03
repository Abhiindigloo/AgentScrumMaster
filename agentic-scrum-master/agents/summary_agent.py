from typing import Any

from agents.base_agent import BaseAgent
from models.standup import StandupUpdate, DailySummary


class SummaryAgent(BaseAgent):
    """Agent responsible for generating daily standup summaries.

    Aggregates individual standup updates into a team-level
    daily summary with blocker highlights and progress overview.
    """

    def __init__(self) -> None:
        super().__init__(name="summary_generator")

    async def process(self, data: dict[str, Any]) -> DailySummary:
        """Generate a daily summary from a collection of standup updates.

        Args:
            data: Dict containing 'updates' (list[StandupUpdate]), 'team_id', and 'date'.

        Returns:
            DailySummary entity with aggregated team information.
        """
        updates: list[StandupUpdate] = data["updates"]
        team_id: str = data["team_id"]
        date: str = data["date"]

        self._log_start(f"team={team_id}, date={date}, count={len(updates)}")

        members_reported = [u.user_name for u in updates]

        all_blockers: list[dict] = []
        for update in updates:
            if update.blocker_detected:
                all_blockers.append({
                    "user_id": update.user_id,
                    "user_name": update.user_name,
                    "blockers": update.blocker_details,
                })

        summary_text = self._build_summary_text(updates, all_blockers)

        summary = DailySummary(
            team_id=team_id,
            date=date,
            total_updates=len(updates),
            members_reported=members_reported,
            blockers_detected=len(all_blockers),
            all_blockers=all_blockers,
            summary=summary_text,
        )

        self._log_complete(f"summary_id={summary.id}")
        return summary

    def _build_summary_text(
        self,
        updates: list[StandupUpdate],
        blockers: list[dict],
    ) -> str:
        """Build a human-readable summary from standup updates."""
        lines: list[str] = []
        lines.append(f"Daily Standup Summary — {len(updates)} member(s) reported.\n")

        lines.append("## Progress")
        for update in updates:
            lines.append(f"- **{update.user_name}**: Yesterday: {update.yesterday}. Today: {update.today}.")

        if blockers:
            lines.append("\n## Blockers")
            for entry in blockers:
                for blocker in entry["blockers"]:
                    lines.append(f"- **{entry['user_name']}**: {blocker}")
        else:
            lines.append("\nNo blockers reported.")

        return "\n".join(lines)
