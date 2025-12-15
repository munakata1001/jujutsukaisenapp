# 予約関連API
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from app.schemas.reservation import (
    ReservationCreate, ReservationUpdate, ReservationResponse
)
from app.services.reservation_service import (
    create_reservation, get_reservation, get_reservation_by_number,
    get_reservations_by_email, get_all_reservations, update_reservation,
    cancel_reservation, search_reservations, complete_reservation,
    get_reservation_with_products
)

router = APIRouter(prefix="/api/reservations", tags=["reservations"])

@router.post("", response_model=ReservationResponse)
async def create_reservation_api(reservation: ReservationCreate):
    """予約を作成"""
    try:
        reservation_data = {
            "user_email": reservation.user_email,
            "user_name": reservation.user_name,
            "user_phone": reservation.user_phone,
            "visit_date": reservation.visit_date,
            "visit_time": reservation.visit_time,
            "products": [{"product_id": p.product_id, "quantity": p.quantity} for p in reservation.products],
        }
        result = await create_reservation(reservation_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約の作成に失敗しました: {str(e)}")

@router.get("/by-number/{reservation_number}", response_model=ReservationResponse)
async def get_reservation_by_number_api(reservation_number: str):
    """予約詳細を取得（予約番号で）"""
    try:
        reservation = await get_reservation_with_products(reservation_number=reservation_number)
        if not reservation:
            raise HTTPException(status_code=404, detail="予約が見つかりません")
        return reservation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約の取得に失敗しました: {str(e)}")

@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation_api(reservation_id: str):
    """予約詳細を取得（IDで）"""
    try:
        reservation = await get_reservation_with_products(reservation_id=reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="予約が見つかりません")
        return reservation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約の取得に失敗しました: {str(e)}")

@router.get("", response_model=List[ReservationResponse])
async def get_reservations_api(
    user_email: Optional[str] = Query(None, description="ユーザーメールアドレス（フィルタ用）"),
    reservation_number: Optional[str] = Query(None, description="予約番号（検索用）"),
    user_name: Optional[str] = Query(None, description="予約者名（検索用）"),
    visit_date: Optional[date] = Query(None, description="来店日（検索用）"),
    status: Optional[str] = Query(None, description="予約ステータス（検索用）"),
    limit: int = Query(100, ge=1, le=1000, description="取得件数上限"),
):
    """予約一覧を取得・検索"""
    try:
        # 検索条件がある場合は検索APIを使用
        if reservation_number or user_name or visit_date or status:
            reservations = await search_reservations(
                reservation_number=reservation_number,
                user_name=user_name,
                visit_date=visit_date,
                status=status,
                limit=limit
            )
        elif user_email:
            # 特定ユーザーの予約一覧
            reservations = await get_reservations_by_email(user_email)
        else:
            # 全予約一覧（管理者用）
            reservations = await get_all_reservations(limit)
        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約一覧の取得に失敗しました: {str(e)}")

@router.put("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation_api(
    reservation_id: str,
    reservation_update: ReservationUpdate,
):
    """予約を更新"""
    try:
        update_data = {}
        if reservation_update.visit_date:
            update_data["visit_date"] = reservation_update.visit_date.isoformat()
        if reservation_update.visit_time:
            update_data["visit_time"] = reservation_update.visit_time
        if reservation_update.products:
            update_data["products"] = [
                {"product_id": p.product_id, "quantity": p.quantity}
                for p in reservation_update.products
            ]
        
        result = await update_reservation(reservation_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail="予約が見つかりません")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約の更新に失敗しました: {str(e)}")

@router.delete("/{reservation_id}", response_model=ReservationResponse)
async def cancel_reservation_api(reservation_id: str):
    """予約をキャンセル"""
    try:
        result = await cancel_reservation(reservation_id)
        if not result:
            raise HTTPException(status_code=404, detail="予約が見つかりません")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約のキャンセルに失敗しました: {str(e)}")

@router.post("/{reservation_id}/complete", response_model=ReservationResponse)
async def complete_reservation_api(reservation_id: str):
    """予約を完了状態に更新"""
    try:
        result = await complete_reservation(reservation_id)
        if not result:
            raise HTTPException(status_code=404, detail="予約が見つかりません")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予約の完了処理に失敗しました: {str(e)}")
