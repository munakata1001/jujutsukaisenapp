# 予約管理サービス
import uuid
from datetime import datetime, date
from typing import List, Optional
from app.utils.firebase import get_firestore_db
from app.services.timeslot_service import (
    increment_reserved_count, decrement_reserved_count,
    generate_slot_id, get_timeslot
)

def generate_reservation_number() -> str:
    """予約番号を生成（例: JJS-2024-XXXXXX）"""
    year = datetime.now().year
    random_part = str(uuid.uuid4().hex[:6]).upper()
    return f"JJS-{year}-{random_part}"

async def create_reservation(reservation_data: dict) -> dict:
    """予約を作成"""
    db = get_firestore_db()
    
    # 予約番号を生成
    reservation_number = generate_reservation_number()
    
    # 予約枠の確認
    slot_id = generate_slot_id(reservation_data["visit_date"], reservation_data["visit_time"])
    timeslot = await get_timeslot(slot_id)
    
    if not timeslot:
        raise ValueError("指定された日時の予約枠が存在しません")
    
    if not timeslot.get("is_available", False):
        raise ValueError("この予約枠は利用できません")
    
    capacity = timeslot.get("capacity", 0)
    reserved = timeslot.get("reserved_count", 0)
    
    if reserved >= capacity:
        raise ValueError("この時間帯は満席です")
    
    # 予約データを作成
    reservation_id = str(uuid.uuid4())
    reservation_doc = {
        "reservation_id": reservation_id,
        "reservation_number": reservation_number,
        "user_email": reservation_data["user_email"],
        "user_name": reservation_data["user_name"],
        "user_phone": reservation_data["user_phone"],
        "visit_date": reservation_data["visit_date"].isoformat() if isinstance(reservation_data["visit_date"], date) else reservation_data["visit_date"],
        "visit_time": reservation_data["visit_time"],
        "status": "confirmed",
        "products": [{"product_id": p["product_id"], "quantity": p["quantity"]} for p in reservation_data.get("products", [])],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    
    # Firestoreに保存
    db.collection("reservations").document(reservation_id).set(reservation_doc)
    
    # 予約枠の予約済み数を増やす
    await increment_reserved_count(slot_id)
    
    return reservation_doc

async def get_reservation(reservation_id: str) -> Optional[dict]:
    """予約を取得"""
    db = get_firestore_db()
    doc = db.collection("reservations").document(reservation_id).get()
    
    if doc.exists:
        return doc.to_dict()
    return None

async def get_reservations_by_email(user_email: str) -> List[dict]:
    """ユーザーの予約一覧を取得"""
    db = get_firestore_db()
    query = db.collection("reservations").where("user_email", "==", user_email)
    docs = query.stream()
    
    reservations = []
    for doc in docs:
        reservations.append(doc.to_dict())
    
    # 作成日時の降順でソート
    reservations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return reservations

async def get_all_reservations(limit: int = 100) -> List[dict]:
    """全予約一覧を取得（管理者用）"""
    db = get_firestore_db()
    # order_byはインデックスが必要なため、簡易実装では作成日時の降順で取得
    query = db.collection("reservations").limit(limit)
    docs = query.stream()
    
    reservations = []
    for doc in docs:
        reservations.append(doc.to_dict())
    
    # メモリ上でソート
    reservations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return reservations

async def update_reservation(reservation_id: str, update_data: dict) -> Optional[dict]:
    """予約を更新"""
    db = get_firestore_db()
    doc_ref = db.collection("reservations").document(reservation_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None
    
    # 日時が変更される場合は、予約枠の予約済み数を調整
    old_data = doc.to_dict()
    if "visit_date" in update_data or "visit_time" in update_data:
        # 古い予約枠の予約済み数を減らす
        old_slot_id = generate_slot_id(
            date.fromisoformat(old_data["visit_date"]),
            old_data["visit_time"]
        )
        await decrement_reserved_count(old_slot_id)
        
        # 新しい予約枠の予約済み数を増やす
        new_date = update_data.get("visit_date", old_data["visit_date"])
        new_time = update_data.get("visit_time", old_data["visit_time"])
        if isinstance(new_date, str):
            new_date = date.fromisoformat(new_date)
        new_slot_id = generate_slot_id(new_date, new_time)
        await increment_reserved_count(new_slot_id)
    
    update_data["updated_at"] = datetime.now().isoformat()
    doc_ref.update(update_data)
    
    return doc_ref.get().to_dict()

async def cancel_reservation(reservation_id: str) -> Optional[dict]:
    """予約をキャンセル"""
    db = get_firestore_db()
    doc_ref = db.collection("reservations").document(reservation_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None
    
    reservation_data = doc.to_dict()
    
    # 予約枠の予約済み数を減らす
    slot_id = generate_slot_id(
        date.fromisoformat(reservation_data["visit_date"]),
        reservation_data["visit_time"]
    )
    await decrement_reserved_count(slot_id)
    
    # ステータスをキャンセルに更新
    doc_ref.update({
        "status": "cancelled",
        "updated_at": datetime.now().isoformat(),
    })
    
    return doc_ref.get().to_dict()

