from abc import ABC, abstractmethod
from typing import Any

from core.logging import get_logger


class BaseAgent(ABC):
    """Base class for all agents in the system.

    Provides a common interface and shared functionality
    for agent implementations. Each agent processes input
    data and returns structured results.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = get_logger(f"agent.{name}")

    @abstractmethod
    async def process(self, data: Any) -> Any:
        """Process input data and return results.

        Args:
            data: Input data specific to the agent type.

        Returns:
            Processed results specific to the agent type.
        """
        ...

    def _log_start(self, context: str) -> None:
        self.logger.info(f"Agent '{self.name}' starting: {context}")

    def _log_complete(self, context: str) -> None:
        self.logger.info(f"Agent '{self.name}' completed: {context}")

    def _log_error(self, context: str, error: Exception) -> None:
        self.logger.error(f"Agent '{self.name}' error in {context}: {error}")
