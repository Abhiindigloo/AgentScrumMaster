from app.agents.standup_agent import StandupAgent
from app.schemas.standup_request import StandupRequest
from app.schemas.standup_response import StandupResponse
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class StandupService:
    """Service layer that orchestrates standup update processing.

    Bridges the API layer and the StandupAgent by converting validated
    request schemas into agent inputs and agent outputs into response schemas.
    """

    def __init__(self, agent: StandupAgent) -> None:
        self._agent = agent

    def process_update(self, request: StandupRequest) -> StandupResponse:
        """Process a single standup update through the agent pipeline.

        Args:
            request: Validated standup request from the API layer.

        Returns:
            Structured response containing analysis results.
        """
        logger.info("Processing standup update for '%s'", request.member_name)

        result = self._agent.analyze_update(
            member_name=request.member_name,
            yesterday=request.yesterday,
            today=request.today,
            blockers=request.blockers,
        )

        response = StandupResponse(**result)

        logger.info(
            "Standup processed for '%s': has_blockers=%s",
            response.member_name,
            response.has_blockers,
        )
        return response
