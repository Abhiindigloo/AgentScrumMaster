from pydantic import BaseModel, Field


class StandupRequest(BaseModel):
    """Schema for a standup update submission."""

    member_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the team member submitting the update.",
    )
    yesterday: str = Field(
        ...,
        min_length=1,
        description="What was accomplished yesterday.",
    )
    today: str = Field(
        ...,
        min_length=1,
        description="What is planned for today.",
    )
    blockers: str | None = Field(
        default=None,
        description="Optional free-text description of blockers or impediments.",
    )
