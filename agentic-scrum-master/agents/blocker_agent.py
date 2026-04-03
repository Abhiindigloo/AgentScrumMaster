import re
from typing import Any

from agents.base_agent import BaseAgent


BLOCKER_KEYWORDS: list[str] = [
    "blocked",
    "blocker",
    "blocking",
    "stuck",
    "waiting on",
    "waiting for",
    "dependent on",
    "dependency",
    "can't proceed",
    "cannot proceed",
    "unable to",
    "no access",
    "access denied",
    "permission",
    "down",
    "outage",
    "broken",
    "failing",
    "failed",
    "timeout",
    "unresolved",
    "pending approval",
    "needs review",
    "on hold",
    "delayed",
    "impediment",
]


class BlockerAgent(BaseAgent):
    """Agent responsible for detecting blockers in standup updates.

    Analyzes the text of standup updates (particularly the blockers field
    and today/yesterday fields) to identify impediments that may affect
    team velocity.
    """

    def __init__(self) -> None:
        super().__init__(name="blocker_detector")

    async def process(self, data: dict[str, Any]) -> dict[str, Any]:
        """Detect blockers from standup update text.

        Args:
            data: Dict containing 'yesterday', 'today', and optionally 'blockers' fields.

        Returns:
            Dict with 'blocker_detected' (bool) and 'blocker_details' (list[str]).
        """
        self._log_start(f"user={data.get('user_id', 'unknown')}")

        detected_blockers: list[str] = []

        blockers_text = data.get("blockers", "") or ""
        if blockers_text.strip():
            extracted = self._extract_blockers(blockers_text)
            detected_blockers.extend(extracted)

        for field_name in ("yesterday", "today"):
            field_text = data.get(field_name, "") or ""
            implicit = self._detect_implicit_blockers(field_text)
            detected_blockers.extend(implicit)

        detected_blockers = list(dict.fromkeys(detected_blockers))

        result = {
            "blocker_detected": len(detected_blockers) > 0,
            "blocker_details": detected_blockers,
        }

        self._log_complete(f"found {len(detected_blockers)} blocker(s)")
        return result

    def _extract_blockers(self, text: str) -> list[str]:
        """Extract individual blocker items from explicit blocker text."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        blockers: list[str] = []

        for line in lines:
            cleaned = re.sub(r"^[-*•]\s*", "", line).strip()
            if cleaned:
                blockers.append(cleaned)

        if not blockers and text.strip():
            blockers.append(text.strip())

        return blockers

    def _detect_implicit_blockers(self, text: str) -> list[str]:
        """Detect implicit blockers from keywords in general text."""
        text_lower = text.lower()
        detected: list[str] = []

        for keyword in BLOCKER_KEYWORDS:
            if keyword in text_lower:
                sentences = re.split(r"[.!?]+", text)
                for sentence in sentences:
                    if keyword in sentence.lower() and sentence.strip():
                        clean = sentence.strip()
                        if clean not in detected:
                            detected.append(clean)
                break

        return detected
