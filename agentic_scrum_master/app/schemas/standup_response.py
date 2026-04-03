from pydantic import BaseModel, Field


class StandupResponse(BaseModel):
    """Schema for the result of a standup update analysis."""

    member_name: str = Field(
        ...,
        description="Name of the team member.",
    )
    normalized_yesterday: str = Field(
        ...,
        description="Cleaned and whitespace-normalized yesterday text.",
    )
    normalized_today: str = Field(
        ...,
        description="Cleaned and whitespace-normalized today text.",
    )
    normalized_blockers: str = Field(
        ...,
        description="Cleaned blocker text, or empty string if none provided.",
    )
    has_blockers: bool = Field(
        ...,
        description="Whether blocker signals were detected in the update.",
    )
    blocker_signals: list[str] = Field(
        ...,
        description="List of blocker keywords found in the update text.",
    )
    blocker_categories: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Matched keywords grouped by category (dependency, environment, approval, technical_issue, delay, unknown).",
    )
    status_summary: str = Field(
        ...,
        description="Concise one-line summary of the standup update.",
    )
