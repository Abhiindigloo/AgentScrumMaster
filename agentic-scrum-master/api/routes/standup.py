from typing import Optional
from fastapi import APIRouter, Depends, Query

from schemas.standup import (
    StandupUpdateRequest,
    StandupUpdateResponse,
    DailySummaryResponse,
    ApiResponse,
)
from services.standup_service import StandupService
from utils.dependencies import get_standup_service

router = APIRouter(prefix="/standups", tags=["standups"])


@router.post("", response_model=ApiResponse, status_code=201)
async def submit_standup(
    request: StandupUpdateRequest,
    service: StandupService = Depends(get_standup_service),
) -> ApiResponse:
    """Submit a new standup update."""
    update = await service.submit_update(request)
    return ApiResponse(
        success=True,
        message="Standup update submitted successfully",
        data=update.to_dict(),
    )


@router.get("/{update_id}", response_model=ApiResponse)
async def get_standup(
    update_id: str,
    service: StandupService = Depends(get_standup_service),
) -> ApiResponse:
    """Retrieve a specific standup update by ID."""
    update = await service.get_update(update_id)
    return ApiResponse(
        success=True,
        message="Standup update retrieved",
        data=update.to_dict(),
    )


@router.get("", response_model=ApiResponse)
async def list_standups(
    team_id: str = Query(default="default", description="Team identifier"),
    date: Optional[str] = Query(default=None, description="Filter by date (YYYY-MM-DD)"),
    service: StandupService = Depends(get_standup_service),
) -> ApiResponse:
    """List standup updates for a team."""
    updates = await service.get_updates_by_team(team_id, date)
    return ApiResponse(
        success=True,
        message=f"Found {len(updates)} standup update(s)",
        data=[u.to_dict() for u in updates],
    )


@router.post("/summary", response_model=ApiResponse)
async def generate_summary(
    team_id: str = Query(default="default", description="Team identifier"),
    date: Optional[str] = Query(default=None, description="Date (YYYY-MM-DD), defaults to today"),
    service: StandupService = Depends(get_standup_service),
) -> ApiResponse:
    """Generate a daily standup summary for a team."""
    summary = await service.generate_daily_summary(team_id, date)
    return ApiResponse(
        success=True,
        message="Daily summary generated",
        data=summary.to_dict(),
    )


@router.get("/summary/{team_id}", response_model=ApiResponse)
async def get_summary(
    team_id: str,
    date: Optional[str] = Query(default=None, description="Date (YYYY-MM-DD)"),
    service: StandupService = Depends(get_standup_service),
) -> ApiResponse:
    """Retrieve a cached daily summary."""
    summary = await service.get_daily_summary(team_id, date)
    return ApiResponse(
        success=True,
        message="Daily summary retrieved",
        data=summary.to_dict(),
    )
