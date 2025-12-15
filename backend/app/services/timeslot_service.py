# 予約枠管理サービス
from datetime import date, datetime, timedelta
from typing import List, Optional
from google.cloud.firestore_v1 import FieldFilter
from app.utils.firebase import get_firestore_db

def generate_slot_id(date_obj: date, time: str) -> str:
    """予約枠IDを生成"""
    date_str = date_obj.isoformat()
    time_str = time.replace(":", "")
    return f"{date_str}_{time_str}"

async def create_timeslot(date_obj: date, time: str, capacity: int) -> dict:
    """予約枠を作成"""
    db = get_firestore_db()
    slot_id = generate_slot_id(date_obj, time)
    
    timeslot_data = {
        "slot_id": slot_id,
        "date": date_obj.isoformat(),
        "time": time,
        "capacity": capacity,
        "reserved_count": 0,
        "is_available": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    
    db.collection("timeslots").document(slot_id).set(timeslot_data)
    return timeslot_data

async def get_timeslot(slot_id: str) -> Optional[dict]:
    """予約枠を取得"""
    db = get_firestore_db()
    doc = db.collection("timeslots").document(slot_id).get()
    
    if doc.exists:
        return doc.to_dict()
    return None

async def get_timeslots_by_date(date_obj: date) -> List[dict]:
    """指定日の予約枠一覧を取得"""
    db = get_firestore_db()
    date_str = date_obj.isoformat()
    
    # 日付でフィルタリング
    query = db.collection("timeslots").where(filter=FieldFilter("date", "==", date_str))
    docs = query.stream()
    
    timeslots = []
    for doc in docs:
        timeslot_data = doc.to_dict()
        timeslots.append(timeslot_data)
    
    # 時間順にソート
    timeslots.sort(key=lambda x: x.get("time", ""))
    return timeslots

async def update_timeslot(slot_id: str, capacity: Optional[int] = None, 
                          is_available: Optional[bool] = None) -> Optional[dict]:
    """予約枠を更新"""
    db = get_firestore_db()
    doc_ref = db.collection("timeslots").document(slot_id)
    
    if not doc_ref.get().exists:
        return None
    
    update_data = {"updated_at": datetime.now().isoformat()}
    if capacity is not None:
        update_data["capacity"] = capacity
    if is_available is not None:
        update_data["is_available"] = is_available
    
    doc_ref.update(update_data)
    return doc_ref.get().to_dict()

async def delete_timeslot(slot_id: str) -> bool:
    """予約枠を削除"""
    db = get_firestore_db()
    doc_ref = db.collection("timeslots").document(slot_id)
    
    if doc_ref.get().exists:
        doc_ref.delete()
        return True
    return False

async def increment_reserved_count(slot_id: str) -> bool:
    """予約済み数を増やす"""
    db = get_firestore_db()
    doc_ref = db.collection("timeslots").document(slot_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return False
    
    current_count = doc.to_dict().get("reserved_count", 0)
    doc_ref.update({
        "reserved_count": current_count + 1,
        "updated_at": datetime.now().isoformat(),
    })
    return True

async def decrement_reserved_count(slot_id: str) -> bool:
    """予約済み数を減らす"""
    db = get_firestore_db()
    doc_ref = db.collection("timeslots").document(slot_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return False
    
    current_count = doc.to_dict().get("reserved_count", 0)
    new_count = max(0, current_count - 1)
    doc_ref.update({
        "reserved_count": new_count,
        "updated_at": datetime.now().isoformat(),
    })
    return True

async def get_timeslots_by_date_range(start_date: date, end_date: date) -> List[dict]:
    """指定期間の予約枠一覧を取得（パフォーマンス最適化）"""
    import logging
    logger = logging.getLogger(__name__)
    
    db = get_firestore_db()
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    
    try:
        # 日付範囲でフィルタリング（一度のクエリで月全体を取得）
        # 同じフィールドに対する範囲クエリ（>= と <=）は通常インデックス不要
        query = db.collection("timeslots").where(
            filter=FieldFilter("date", ">=", start_date_str)
        ).where(
            filter=FieldFilter("date", "<=", end_date_str)
        )
        docs = query.stream()
        
        timeslots = []
        for doc in docs:
            timeslot_data = doc.to_dict()
            timeslots.append(timeslot_data)
        
        # 日付順、時間順にソート
        timeslots.sort(key=lambda x: (x.get("date", ""), x.get("time", "")))
        return timeslots
    except Exception as e:
        error_msg = str(e)
        logger.error(f"get_timeslots_by_date_rangeエラー: {error_msg}")
        
        # インデックスエラーの場合は、フォールバック処理を使用
        if "index" in error_msg.lower() or "requires an index" in error_msg.lower():
            logger.warning("複合インデックスが必要です。フォールバック処理を使用します。")
            # フォールバック: 各日ごとにクエリ（以前の実装）
            all_timeslots = []
            current_date = start_date
            while current_date <= end_date:
                try:
                    day_timeslots = await get_timeslots_by_date(current_date)
                    all_timeslots.extend(day_timeslots)
                except Exception as day_error:
                    logger.warning(f"日付 {current_date} の取得に失敗: {day_error}")
                # 次の日へ
                current_date += timedelta(days=1)
            return all_timeslots
        else:
            # その他のエラーは再スロー
            raise

async def get_calendar_data(year: int, month: int) -> dict:
    """カレンダーデータを取得（月次）- パフォーマンス最適化版"""
    import logging
    from calendar import monthrange
    
    logger = logging.getLogger(__name__)
    
    days_in_month = monthrange(year, month)[1]
    calendar_data = {}
    
    # 月の開始日と終了日を計算
    start_date = date(year, month, 1)
    end_date = date(year, month, days_in_month)
    
    try:
        # 月全体の予約枠を一度のクエリで取得（パフォーマンス改善）
        all_timeslots = await get_timeslots_by_date_range(start_date, end_date)
    except Exception as e:
        logger.error(f"get_calendar_dataエラー: {str(e)}")
        raise
    
    # 日付ごとにグループ化
    timeslots_by_date = {}
    for slot in all_timeslots:
        slot_date_str = slot.get("date")
        if not slot_date_str:
            continue
        
        slot_date = date.fromisoformat(slot_date_str) if isinstance(slot_date_str, str) else slot_date_str
        date_key = slot_date.isoformat()
        
        if date_key not in timeslots_by_date:
            timeslots_by_date[date_key] = []
        timeslots_by_date[date_key].append(slot)
    
    # 各日の予約可能枠数を計算
    for day in range(1, days_in_month + 1):
        date_obj = date(year, month, day)
        date_key = date_obj.isoformat()
        timeslots = timeslots_by_date.get(date_key, [])
        
        if not timeslots:
            calendar_data[day] = {"status": "unavailable", "availableSlots": 0}
            continue
        
        # 予約可能枠数を計算
        available_slots = 0
        for slot in timeslots:
            if slot.get("is_available", False):
                capacity = slot.get("capacity", 0)
                reserved = slot.get("reserved_count", 0)
                available_slots += max(0, capacity - reserved)
        
        # ステータスを決定
        if available_slots == 0:
            status = "full"
        elif available_slots <= 2:
            status = "limited"
        else:
            status = "available"
        
        calendar_data[day] = {
            "status": status,
            "availableSlots": available_slots,
        }
    
    return calendar_data

async def get_timeslot_stats() -> dict:
    """予約状況統計を取得"""
    from datetime import date, timedelta
    db = get_firestore_db()
    
    # 今日から30日先までの予約枠を取得
    today = date.today()
    end_date = today + timedelta(days=30)
    
    stats = {
        "total_slots": 0,
        "total_capacity": 0,
        "total_reserved": 0,
        "available_slots": 0,
        "full_slots": 0,
        "by_date": {},
    }
    
    # 予約枠を日付ごとに集計
    query = db.collection("timeslots")
    docs = query.stream()
    
    for doc in docs:
        timeslot_data = doc.to_dict()
        slot_date_str = timeslot_data.get("date")
        if not slot_date_str:
            continue
        
        slot_date = date.fromisoformat(slot_date_str) if isinstance(slot_date_str, str) else slot_date_str
        if slot_date < today or slot_date > end_date:
            continue
        
        capacity = timeslot_data.get("capacity", 0)
        reserved = timeslot_data.get("reserved_count", 0)
        is_available = timeslot_data.get("is_available", False)
        
        if not is_available:
            continue
        
        stats["total_slots"] += 1
        stats["total_capacity"] += capacity
        stats["total_reserved"] += reserved
        
        available_count = max(0, capacity - reserved)
        stats["available_slots"] += available_count
        
        if reserved >= capacity:
            stats["full_slots"] += 1
        
        # 日付ごとの統計
        date_key = slot_date.isoformat()
        if date_key not in stats["by_date"]:
            stats["by_date"][date_key] = {
                "total_slots": 0,
                "total_capacity": 0,
                "total_reserved": 0,
                "available_slots": 0,
                "full_slots": 0,
            }
        
        stats["by_date"][date_key]["total_slots"] += 1
        stats["by_date"][date_key]["total_capacity"] += capacity
        stats["by_date"][date_key]["total_reserved"] += reserved
        stats["by_date"][date_key]["available_slots"] += available_count
        if reserved >= capacity:
            stats["by_date"][date_key]["full_slots"] += 1
    
    # 予約率を計算
    if stats["total_capacity"] > 0:
        stats["reservation_rate"] = round((stats["total_reserved"] / stats["total_capacity"]) * 100, 2)
    else:
        stats["reservation_rate"] = 0
    
    return stats

