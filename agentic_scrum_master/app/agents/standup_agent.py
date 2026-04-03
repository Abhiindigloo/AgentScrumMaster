import re
from typing import Any

from app.core.logging_config import get_logger

logger = get_logger(__name__)

BLOCKER_KEYWORDS: list[str] = [
    "blocked",
    "blocker",
    "stuck",
    "dependency",
    "waiting",
    "issue",
    "delayed",
]


class StandupAgent:
    """Agent responsible for analyzing a single team member's standup update.

    Accepts structured standup input, normalizes text, extracts key fields,
    detects blocker signals, and returns a structured result dictionary.
    All logic is deterministic — no external LLM calls.
    """

    def analyze_update(
        self,
        member_name: str,
        yesterday: str,
        today: str,
        blockers: str | None = None,
    ) -> dict[str, Any]:
        """Analyze a standup update and return structured results.

        Args:
            member_name: Name of the team member submitting the update.
            yesterday:   What the member accomplished yesterday.
            today:       What the member plans to do today.
            blockers:    Optional free-text description of blockers.

        Returns:
            Dictionary containing normalized fields, blocker detection
            results, and a concise status summary.
        """
        logger.info("Analyzing standup update for '%s'", member_name)

        normalized_yesterday = self._normalize_text(yesterday)
        normalized_today = self._normalize_text(today)
        normalized_blockers = self._normalize_text(blockers) if blockers else ""

        blocker_signals = self._detect_blocker_signals(
            normalized_yesterday,
            normalized_today,
            normalized_blockers,
        )
        has_blockers = len(blocker_signals) > 0

        status_summary = self._build_status_summary(
            member_name,
            normalized_yesterday,
            normalized_today,
            has_blockers,
            blocker_signals,
        )

        result: dict[str, Any] = {
            "member_name": member_name,
            "normalized_yesterday": normalized_yesterday,
            "normalized_today": normalized_today,
            "normalized_blockers": normalized_blockers,
            "has_blockers": has_blockers,
            "blocker_signals": blocker_signals,
            "status_summary": status_summary,
        }

        logger.info(
            "Standup analysis complete for '%s': has_blockers=%s, signals=%d",
            member_name,
            has_blockers,
            len(blocker_signals),
        )
        return result

    def _normalize_text(self, text: str) -> str:
        """Collapse whitespace and strip leading/trailing spaces."""
        return re.sub(r"\s+", " ", text).strip()

    def _detect_blocker_signals(
        self,
        yesterday: str,
        today: str,
        blockers: str,
    ) -> list[str]:
        """Scan all fields for blocker keywords and return matched signals."""
        combined = f"{yesterday} {today} {blockers}".lower()
        return [kw for kw in BLOCKER_KEYWORDS if kw in combined]

    def _build_status_summary(
        self,
        member_name: str,
        yesterday: str,
        today: str,
        has_blockers: bool,
        blocker_signals: list[str],
    ) -> str:
        """Produce a concise, deterministic one-line status summary."""
        yesterday_snippet = self._truncate(yesterday, 60)
        today_snippet = self._truncate(today, 60)

        summary = f"{member_name}: Yesterday — {yesterday_snippet}. Today — {today_snippet}."

        if has_blockers:
            signals_str = ", ".join(blocker_signals)
            summary += f" [BLOCKER: {signals_str}]"

        return summary

    def _truncate(self, text: str, max_length: int) -> str:
        """Truncate text to max_length, appending '...' if shortened."""
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."
