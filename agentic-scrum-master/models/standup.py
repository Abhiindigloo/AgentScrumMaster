from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class StandupUpdate:
    """Domain entity representing a standup update."""

    user_id: str
    user_name: str
    yesterday: str
    today: str
    team_id: str = "default"
    sprint_id: Optional[str] = None
    blockers: Optional[str] = None
    blocker_detected: bool = False
    blocker_details: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "team_id": self.team_id,
            "sprint_id": self.sprint_id,
            "yesterday": self.yesterday,
            "today": self.today,
            "blockers": self.blockers,
            "blocker_detected": self.blocker_detected,
            "blocker_details": self.blocker_details,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class DailySummary:
    """Domain entity representing a daily standup summary."""

    team_id: str
    date: str
    total_updates: int
    members_reported: list[str]
    blockers_detected: int
    all_blockers: list[dict]
    summary: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": self.id,
            "team_id": self.team_id,
            "date": self.date,
            "total_updates": self.total_updates,
            "members_reported": self.members_reported,
            "blockers_detected": self.blockers_detected,
            "all_blockers": self.all_blockers,
            "summary": self.summary,
            "created_at": self.created_at.isoformat(),
        }
