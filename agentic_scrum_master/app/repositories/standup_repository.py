from datetime import datetime, timezone
from typing import Protocol
from dataclasses import dataclass, field
import uuid


@dataclass
class StandupRecord:
    """Stored representation of a standup update."""

    id: str
    member_name: str
    normalized_yesterday: str
    normalized_today: str
    normalized_blockers: str
    has_blockers: bool
    blocker_signals: list[str]
    status_summary: str
    created_at: datetime


class StandupRepository(Protocol):
    """Interface that any standup storage backend must implement."""

    def save_update(self, record: StandupRecord) -> StandupRecord: ...

    def get_updates_by_member(self, member_name: str) -> list[StandupRecord]: ...

    def get_all_updates(self) -> list[StandupRecord]: ...


class InMemoryStandupRepository:
    """In-memory implementation of StandupRepository.

    Stores records in a plain dictionary keyed by ID.
    Suitable for development and testing; swap with a
    database-backed implementation for production.
    """

    def __init__(self) -> None:
        self._store: dict[str, StandupRecord] = {}

    def save_update(self, record: StandupRecord) -> StandupRecord:
        """Persist a standup record and return it."""
        self._store[record.id] = record
        return record

    def get_updates_by_member(self, member_name: str) -> list[StandupRecord]:
        """Return all records for a given member, newest first."""
        return sorted(
            [r for r in self._store.values() if r.member_name == member_name],
            key=lambda r: r.created_at,
            reverse=True,
        )

    def get_all_updates(self) -> list[StandupRecord]:
        """Return every stored record, newest first."""
        return sorted(
            self._store.values(),
            key=lambda r: r.created_at,
            reverse=True,
        )


def create_standup_record(
    member_name: str,
    normalized_yesterday: str,
    normalized_today: str,
    normalized_blockers: str,
    has_blockers: bool,
    blocker_signals: list[str],
    status_summary: str,
) -> StandupRecord:
    """Factory function to build a StandupRecord with generated id and timestamp."""
    return StandupRecord(
        id=str(uuid.uuid4()),
        member_name=member_name,
        normalized_yesterday=normalized_yesterday,
        normalized_today=normalized_today,
        normalized_blockers=normalized_blockers,
        has_blockers=has_blockers,
        blocker_signals=blocker_signals,
        status_summary=status_summary,
        created_at=datetime.now(timezone.utc),
    )
