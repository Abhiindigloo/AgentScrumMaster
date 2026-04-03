from fastapi import APIRouter

from app.agents.standup_agent import StandupAgent
from app.services.standup_service import StandupService
from app.schemas.standup_request import StandupRequest
from app.schemas.standup_response import StandupResponse

router = APIRouter(prefix="/api/v1/standup", tags=["standup"])

_service = StandupService(agent=StandupAgent())


@router.post("/analyze", response_model=StandupResponse, status_code=200)
async def analyze_standup(request: StandupRequest) -> StandupResponse:
    """Analyze a single standup update and return structured results."""
    return _service.process_update(request)
