# 予約枠関連API
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List
from datetime import date
from app.schemas.timeslot import (
    TimeSlotCreate, TimeSlotUpdate, TimeSlotResponse, AvailabilityResponse
)
from app.services.timeslot_service import (
    create_timeslot, get_timeslot, get_timeslots_by_date,
    update_timeslot, delete_timeslot, generate_slot_id
)

router = APIRouter(prefix="/api/timeslots", tags=["timeslots"])

@router.get("", response_model=List[TimeSlotResponse])
async def get_timeslots(
    date_param: date = Query(..., alias="date", description="日付"),
):
    """指定日の予約可能枠を取得"""
    try:
        timeslots = await get_timeslots_by_date(date_param)
        return timeslots
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約可能枠の取得に失敗しました: {str(e)}")

@router.get("/availability", response_model=AvailabilityResponse)
async def check_availability(
    date_param: date = Query(..., alias="date", description="日付"),
    time: str = Query(..., pattern=r"^\d{2}:\d{2}$", description="時間（HH:MM形式）"),
):
    """空き状況を確認"""
    try:
        slot_id = generate_slot_id(date_param, time)
        timeslot = await get_timeslot(slot_id)
        
        if not timeslot:
            return AvailabilityResponse(
                available=False,
                available_count=0,
                capacity=0,
                reserved_count=0,
            )
        
        capacity = timeslot.get("capacity", 0)
        reserved = timeslot.get("reserved_count", 0)
        available_count = max(0, capacity - reserved)
        
        return AvailabilityResponse(
            available=timeslot.get("is_available", False) and available_count > 0,
            available_count=available_count,
            capacity=capacity,
            reserved_count=reserved,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"空き状況の確認に失敗しました: {str(e)}")

# 管理者用API
admin_router = APIRouter(prefix="/api/admin/timeslots", tags=["admin-timeslots"])

@admin_router.post("", response_model=TimeSlotResponse)
async def create_timeslot_admin(timeslot: TimeSlotCreate):
    """予約枠を作成（管理者）"""
    try:
        result = await create_timeslot(
            timeslot.date,
            timeslot.time,
            timeslot.capacity,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"予約枠の作成に失敗しました: {str(e)}")

@admin_router.put("/{slot_id}", response_model=TimeSlotResponse)
async def update_timeslot_admin(
    slot_id: str,
    timeslot_update: TimeSlotUpdate,
):
    """予約枠を更新（管理者）"""
    try:
        result = await update_timeslot(
            slot_id,
            capacity=timeslot_update.capacity,
            is_available=timeslot_update.is_available,
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="予約枠が見つかりません")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約枠の更新に失敗しました: {str(e)}")

@admin_router.delete("/{slot_id}")
async def delete_timeslot_admin(slot_id: str):
    """予約枠を削除（管理者）"""
    try:
        success = await delete_timeslot(slot_id)
        if not success:
            raise HTTPException(status_code=404, detail="予約枠が見つかりません")
        return {"message": "予約枠を削除しました"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約枠の削除に失敗しました: {str(e)}")

@admin_router.get("/stats")
async def get_timeslot_stats():
    """予約状況統計を取得（管理者）"""
    # 実装は簡略化（必要に応じて拡張）
    return {"message": "統計機能は今後実装予定です"}

