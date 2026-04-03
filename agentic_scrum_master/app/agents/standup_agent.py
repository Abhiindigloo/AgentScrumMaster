import re
from typing import Any

from app.core.logging_config import get_logger

logger = get_logger(__name__)

BLOCKER_CATEGORY_MAP: dict[str, list[str]] = {
    "dependency": [
        "dependency",
        "dependent on",
        "depends on",
        "waiting for",
        "waiting on",
        "need from",
        "needs from",
        "upstream",
    ],
    "environment": [
        "environment",
        "staging",
        "production",
        "infra",
        "infrastructure",
        "server down",
        "outage",
        "deployment",
        "pipeline",
        "ci/cd",
        "no access",
        "access denied",
        "permission",
        "credentials",
        "vpn",
    ],
    "approval": [
        "approval",
        "pending review",
        "needs review",
        "pending sign-off",
        "sign-off",
        "waiting for approval",
        "manager",
    ],
    "technical_issue": [
        "bug",
        "broken",
        "failing",
        "failed",
        "crash",
        "error",
        "exception",
        "timeout",
        "flaky",
        "issue",
    ],
    "delay": [
        "delayed",
        "postponed",
        "on hold",
        "pushed back",
        "rescheduled",
        "slipped",
    ],
}

GENERAL_BLOCKER_KEYWORDS: list[str] = [
    "blocked",
    "blocker",
    "stuck",
    "cannot proceed",
    "can't proceed",
    "impediment",
]


class StandupAgent:
    """Agent responsible for analyzing a single team member's standup update.

    Accepts structured standup input, normalizes text, extracts key fields,
    detects and categorizes blocker signals, and returns a structured result.
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
            results (with categories), and a concise status summary.
        """
        logger.info("Analyzing standup update for '%s'", member_name)

        normalized_yesterday = self._normalize_text(yesterday)
        normalized_today = self._normalize_text(today)
        normalized_blockers = self._normalize_text(blockers) if blockers else ""

        blocker_signals, blocker_categories = self._detect_blocker_signals(
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
            "blocker_categories": blocker_categories,
            "status_summary": status_summary,
        }

        logger.info(
            "Standup analysis complete for '%s': has_blockers=%s, signals=%d, categories=%s",
            member_name,
            has_blockers,
            len(blocker_signals),
            list(blocker_categories.keys()),
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
    ) -> tuple[list[str], dict[str, list[str]]]:
        """Scan all fields for blocker keywords, returning signals and categories.

        Returns:
            A tuple of (flat signal list, category-to-keywords mapping).
        """
        combined = f"{yesterday} {today} {blockers}".lower()
        matched_signals: list[str] = []
        categories: dict[str, list[str]] = {}

        for category, keywords in BLOCKER_CATEGORY_MAP.items():
            hits = [kw for kw in keywords if kw in combined]
            if hits:
                matched_signals.extend(hits)
                categories[category] = hits

        general_hits = [kw for kw in GENERAL_BLOCKER_KEYWORDS if kw in combined]
        if general_hits:
            matched_signals.extend(general_hits)

        if matched_signals and not categories:
            categories["unknown"] = general_hits or matched_signals[:1]

        matched_signals = list(dict.fromkeys(matched_signals))

        return matched_signals, categories

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
