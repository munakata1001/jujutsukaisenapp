# カレンダー関連API
import logging
from fastapi import APIRouter, HTTPException, Query
from app.schemas.calendar import CalendarDataResponse
from app.services.timeslot_service import get_calendar_data

logger = logging.getLogger(__name__)

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
        error_msg = str(e)
        logger.error(f"カレンダーデータ取得エラー (year={year}, month={month}): {error_msg}", exc_info=True)
        
        # インデックスエラーの場合は、より分かりやすいメッセージを返す
        if "index" in error_msg.lower() or "requires an index" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail=f"カレンダーデータの取得に失敗しました: Firestoreの複合インデックスが必要です。エラーメッセージに表示されたURLからインデックスを作成してください。エラー詳細: {error_msg}"
            )
        
        raise HTTPException(status_code=500, detail=f"カレンダーデータの取得に失敗しました: {error_msg}")



