from functools import lru_cache

from services.standup_service import StandupService


@lru_cache()
def get_standup_service() -> StandupService:
    """Dependency provider for StandupService singleton."""
    return StandupService()
