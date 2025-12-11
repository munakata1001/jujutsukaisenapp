# カレンダー関連API
from fastapi import APIRouter, HTTPException, Query
from app.schemas.calendar import CalendarDataResponse
from app.services.timeslot_service import get_calendar_data

router = APIRouter(prefix="/api/calendar", tags=["calendar"])

@router.get("", response_model=CalendarDataResponse)
async def get_calendar(
    year: int = Query(..., description="年"),
    month: int = Query(..., ge=1, le=12, description="月（1-12）"),
):
    """カレンダーデータを取得（月次）"""
    try:
        data = await get_calendar_data(year, month)
        return CalendarDataResponse(
            year=year,
            month=month,
            data=data,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"カレンダーデータの取得に失敗しました: {str(e)}")

