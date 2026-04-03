from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StandupUpdateRequest(BaseModel):
    """Schema for submitting a standup update."""

    user_id: str = Field(..., min_length=1, max_length=100, description="Unique identifier of the team member")
    user_name: str = Field(..., min_length=1, max_length=200, description="Display name of the team member")
    team_id: str = Field(default="default", max_length=100, description="Team identifier")
    sprint_id: Optional[str] = Field(default=None, max_length=100, description="Current sprint identifier")
    yesterday: str = Field(..., min_length=1, description="What was accomplished yesterday")
    today: str = Field(..., min_length=1, description="What is planned for today")
    blockers: Optional[str] = Field(default=None, description="Any blockers or impediments")


class StandupUpdateResponse(BaseModel):
    """Schema for standup update response."""

    id: str = Field(..., description="Unique identifier of the standup update")
    user_id: str
    user_name: str
    team_id: str
    sprint_id: Optional[str]
    yesterday: str
    today: str
    blockers: Optional[str]
    blocker_detected: bool = Field(default=False, description="Whether blockers were detected")
    blocker_details: list[str] = Field(default_factory=list, description="Extracted blocker details")
    created_at: datetime


class DailySummaryResponse(BaseModel):
    """Schema for daily standup summary."""

    team_id: str
    date: str
    total_updates: int
    members_reported: list[str]
    blockers_detected: int
    all_blockers: list[dict]
    summary: str
    created_at: datetime


class ApiResponse(BaseModel):
    """Standard API response wrapper."""

    success: bool = True
    message: str = ""
    data: Optional[dict | list] = None
