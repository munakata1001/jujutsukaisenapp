# 予約枠管理サービス
from datetime import date, datetime
from typing import List, Optional
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
    query = db.collection("timeslots").where("date", "==", date_str)
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

async def get_calendar_data(year: int, month: int) -> dict:
    """カレンダーデータを取得（月次）"""
    from calendar import monthrange
    
    db = get_firestore_db()
    days_in_month = monthrange(year, month)[1]
    calendar_data = {}
    
    # 各日の予約枠を取得
    for day in range(1, days_in_month + 1):
        date_obj = date(year, month, day)
        timeslots = await get_timeslots_by_date(date_obj)
        
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

