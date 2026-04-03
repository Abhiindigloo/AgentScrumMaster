from dataclasses import dataclass, field

from app.schemas.standup_response import StandupResponse
from app.core.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class TeamStandupSummary:
    """Aggregated summary of a team's daily standup."""

    total_members: int
    members_with_blockers: int
    blocker_count: int
    blocker_category_counts: dict[str, int]
    concise_team_summary: str
    member_summaries: list[dict[str, str]]


class StandupSummaryService:
    """Combines individual standup responses into a team-level daily summary.

    All logic is deterministic — no LLM calls.
    Output is structured for easy consumption by Slack, Jira, or other reporters.
    """

    def generate_team_summary(
        self, responses: list[StandupResponse]
    ) -> TeamStandupSummary:
        """Build a team summary from a list of processed standup responses.

        Args:
            responses: Individual standup analysis results.

        Returns:
            Aggregated team summary with blocker statistics and per-member entries.
        """
        logger.info("Generating team summary for %d member(s)", len(responses))

        blocked_members = [r for r in responses if r.has_blockers]
        blocker_count = sum(len(r.blocker_signals) for r in responses)

        blocker_category_counts: dict[str, int] = {}
        for r in responses:
            for category, keywords in r.blocker_categories.items():
                blocker_category_counts[category] = (
                    blocker_category_counts.get(category, 0) + len(keywords)
                )

        member_summaries = [
            self._build_member_entry(r) for r in responses
        ]

        concise_team_summary = self._build_concise_summary(
            total=len(responses),
            blocked=len(blocked_members),
            blocker_count=blocker_count,
            blocked_names=[r.member_name for r in blocked_members],
        )

        summary = TeamStandupSummary(
            total_members=len(responses),
            members_with_blockers=len(blocked_members),
            blocker_count=blocker_count,
            blocker_category_counts=blocker_category_counts,
            concise_team_summary=concise_team_summary,
            member_summaries=member_summaries,
        )

        logger.info(
            "Team summary complete: %d members, %d blocked, %d signals",
            summary.total_members,
            summary.members_with_blockers,
            summary.blocker_count,
        )
        return summary

    def _build_member_entry(self, response: StandupResponse) -> dict[str, str]:
        """Create a per-member summary dict from a standup response."""
        entry: dict[str, str] = {
            "member_name": response.member_name,
            "status_summary": response.status_summary,
            "blocker_status": "blocked" if response.has_blockers else "clear",
        }
        if response.has_blockers:
            entry["blocker_details"] = response.normalized_blockers or ", ".join(
                response.blocker_signals
            )
            entry["blocker_categories"] = ", ".join(response.blocker_categories.keys())
        return entry

    def _build_concise_summary(
        self,
        total: int,
        blocked: int,
        blocker_count: int,
        blocked_names: list[str],
    ) -> str:
        """Produce a deterministic one-paragraph team summary."""
        if total == 0:
            return "No standup updates submitted."

        parts: list[str] = [f"Team standup: {total} member(s) reported."]

        if blocked == 0:
            parts.append("No blockers detected.")
        else:
            names = ", ".join(blocked_names)
            parts.append(
                f"{blocked} member(s) blocked ({blocker_count} signal(s)): {names}."
            )

        return " ".join(parts)
