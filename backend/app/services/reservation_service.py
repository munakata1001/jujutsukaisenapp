# 予約管理サービス
import uuid
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Tuple
from google.cloud.firestore_v1 import FieldFilter
from app.utils.firebase import get_firestore_db
from app.services.timeslot_service import (
    increment_reserved_count, decrement_reserved_count,
    generate_slot_id, get_timeslot
)
from app.services.product_service import (
    increment_order_count, decrement_order_count
)

def generate_reservation_number() -> str:
    """予約番号を生成（例: JJS-2024-XXXXXX）"""
    year = datetime.now().year
    random_part = str(uuid.uuid4().hex[:6]).upper()
    return f"JJS-{year}-{random_part}"

async def check_product_limits(products: List[dict], user_email: str) -> None:
    """購入制限をチェック"""
    db = get_firestore_db()
    
    for product_item in products:
        product_id = product_item["product_id"]
        quantity = product_item["quantity"]
        
        # 商品情報を取得
        product_doc = db.collection("products").document(product_id).get()
        if not product_doc.exists:
            raise ValueError(f"商品ID {product_id} が見つかりません")
        
        product_data = product_doc.to_dict()
        
        # 1予約あたりの最大購入数チェック
        max_per_reservation = product_data.get("max_per_reservation", 0)
        if max_per_reservation > 0 and quantity > max_per_reservation:
            raise ValueError(f"商品 {product_data.get('name', product_id)} は1予約あたり最大{max_per_reservation}個まで購入可能です")
        
        # 受注期間チェック
        order_start = product_data.get("order_start_date")
        order_end = product_data.get("order_end_date")
        today = date.today()
        
        if order_start:
            start_date = date.fromisoformat(order_start) if isinstance(order_start, str) else order_start
            if today < start_date:
                raise ValueError(f"商品 {product_data.get('name', product_id)} の受注期間はまだ開始していません")
        
        if order_end:
            end_date = date.fromisoformat(order_end) if isinstance(order_end, str) else order_end
            if today > end_date:
                raise ValueError(f"商品 {product_data.get('name', product_id)} の受注期間は終了しています")
        
        # 総受注数の上限チェック
        total_order_limit = product_data.get("total_order_limit")
        if total_order_limit and total_order_limit > 0:
            # current_order_countを使用（予約作成時に更新される）
            current_count = product_data.get("current_order_count", 0)
            
            if current_count + quantity > total_order_limit:
                raise ValueError(f"商品 {product_data.get('name', product_id)} の受注上限に達しています（残り{total_order_limit - current_count}個）")

async def create_reservation(reservation_data: dict) -> dict:
    """予約を作成"""
    db = get_firestore_db()
    
    # 予約番号を生成
    reservation_number = generate_reservation_number()
    
    # 予約枠の確認
    visit_date = reservation_data["visit_date"]
    if isinstance(visit_date, str):
        visit_date = date.fromisoformat(visit_date)
    
    slot_id = generate_slot_id(visit_date, reservation_data["visit_time"])
    timeslot = await get_timeslot(slot_id)
    
    if not timeslot:
        raise ValueError("指定された日時の予約枠が存在しません")
    
    if not timeslot.get("is_available", False):
        raise ValueError("この予約枠は利用できません")
    
    capacity = timeslot.get("capacity", 0)
    reserved = timeslot.get("reserved_count", 0)
    
    if reserved >= capacity:
        raise ValueError("この時間帯は満席です")
    
    # 購入制限チェック
    products = reservation_data.get("products", [])
    if products:
        await check_product_limits(products, reservation_data["user_email"])
    
    # 予約データを作成
    reservation_id = str(uuid.uuid4())
    reservation_doc = {
        "reservation_id": reservation_id,
        "reservation_number": reservation_number,
        "user_email": reservation_data["user_email"],
        "user_name": reservation_data["user_name"],
        "user_phone": reservation_data["user_phone"],
        "visit_date": visit_date.isoformat(),
        "visit_time": reservation_data["visit_time"],
        "status": "confirmed",
        "products": [{"product_id": p["product_id"], "quantity": p["quantity"]} for p in products],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    
    # Firestoreに保存
    db.collection("reservations").document(reservation_id).set(reservation_doc)
    
    # 予約枠の予約済み数を増やす
    await increment_reserved_count(slot_id)
    
    # 商品の受注数を増やす
    for product_item in products:
        await increment_order_count(product_item["product_id"], product_item["quantity"])
    
    return reservation_doc

async def get_reservation(reservation_id: str) -> Optional[dict]:
    """予約を取得（IDで）"""
    db = get_firestore_db()
    doc = db.collection("reservations").document(reservation_id).get()
    
    if doc.exists:
        return doc.to_dict()
    return None

async def get_reservation_by_number(reservation_number: str) -> Optional[dict]:
    """予約を取得（予約番号で）"""
    db = get_firestore_db()
    query = db.collection("reservations").where(
        filter=FieldFilter("reservation_number", "==", reservation_number)
    ).limit(1)
    docs = list(query.stream())
    
    if docs:
        return docs[0].to_dict()
    return None

async def get_reservations_by_email(user_email: str) -> List[dict]:
    """ユーザーの予約一覧を取得"""
    db = get_firestore_db()
    query = db.collection("reservations").where(
        filter=FieldFilter("user_email", "==", user_email)
    )
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

async def can_modify_reservation(visit_date: date) -> bool:
    """予約変更が可能かチェック（来店日の前日まで変更可能）"""
    today = date.today()
    # 来店日の前日まで変更可能
    return visit_date > today + timedelta(days=1)

async def update_reservation(reservation_id: str, update_data: dict) -> Optional[dict]:
    """予約を更新"""
    db = get_firestore_db()
    doc_ref = db.collection("reservations").document(reservation_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None
    
    old_data = doc.to_dict()
    
    # キャンセル済みの予約は変更不可
    if old_data.get("status") == "cancelled":
        raise ValueError("キャンセル済みの予約は変更できません")
    
    # 日時変更の制約チェック
    if "visit_date" in update_data or "visit_time" in update_data:
        old_visit_date = date.fromisoformat(old_data["visit_date"])
        if not await can_modify_reservation(old_visit_date):
            raise ValueError("予約変更は来店日の前日まで可能です")
        
        # 新しい予約枠の確認
        new_date = update_data.get("visit_date", old_data["visit_date"])
        new_time = update_data.get("visit_time", old_data["visit_time"])
        if isinstance(new_date, str):
            new_date = date.fromisoformat(new_date)
        
        new_slot_id = generate_slot_id(new_date, new_time)
        new_timeslot = await get_timeslot(new_slot_id)
        
        if not new_timeslot:
            raise ValueError("変更先の予約枠が存在しません")
        
        if not new_timeslot.get("is_available", False):
            raise ValueError("変更先の予約枠は利用できません")
        
        capacity = new_timeslot.get("capacity", 0)
        reserved = new_timeslot.get("reserved_count", 0)
        
        if reserved >= capacity:
            raise ValueError("変更先の時間帯は満席です")
        
        # 古い予約枠の予約済み数を減らす
        old_slot_id = generate_slot_id(
            date.fromisoformat(old_data["visit_date"]),
            old_data["visit_time"]
        )
        await decrement_reserved_count(old_slot_id)
        
        # 新しい予約枠の予約済み数を増やす
        await increment_reserved_count(new_slot_id)
        
        # 古い商品の受注数を減らす
        old_products = old_data.get("products", [])
        for product_item in old_products:
            await decrement_order_count(product_item["product_id"], product_item["quantity"])
        
        # 新しい商品の受注数を増やす
        new_products = update_data.get("products", [])
        for product_item in new_products:
            await increment_order_count(product_item["product_id"], product_item["quantity"])
    
    # 商品変更時の購入制限チェック
    if "products" in update_data:
        products = update_data["products"]
        if isinstance(products, list) and len(products) > 0:
            # 辞書形式に変換
            product_list = []
            for p in products:
                if isinstance(p, dict):
                    product_list.append(p)
                else:
                    product_list.append({"product_id": p.product_id, "quantity": p.quantity})
            await check_product_limits(product_list, old_data["user_email"])
    
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
    
    # 既にキャンセル済みの場合はエラー
    if reservation_data.get("status") == "cancelled":
        raise ValueError("この予約は既にキャンセル済みです")
    
    # 予約枠の予約済み数を減らす
    slot_id = generate_slot_id(
        date.fromisoformat(reservation_data["visit_date"]),
        reservation_data["visit_time"]
    )
    await decrement_reserved_count(slot_id)
    
    # 商品の受注数を減らす
    products = reservation_data.get("products", [])
    for product_item in products:
        await decrement_order_count(product_item["product_id"], product_item["quantity"])
    
    # ステータスをキャンセルに更新
    doc_ref.update({
        "status": "cancelled",
        "updated_at": datetime.now().isoformat(),
    })
    
    return doc_ref.get().to_dict()

async def search_reservations(
    reservation_number: Optional[str] = None,
    user_name: Optional[str] = None,
    visit_date: Optional[date] = None,
    status: Optional[str] = None,
    limit: int = 100
) -> List[dict]:
    """予約を検索"""
    db = get_firestore_db()
    query = db.collection("reservations")
    
    # 検索条件を適用
    if reservation_number:
        query = query.where(filter=FieldFilter("reservation_number", "==", reservation_number))
    if user_name:
        query = query.where(filter=FieldFilter("user_name", "==", user_name))
    if visit_date:
        date_str = visit_date.isoformat() if isinstance(visit_date, date) else visit_date
        query = query.where(filter=FieldFilter("visit_date", "==", date_str))
    if status:
        query = query.where(filter=FieldFilter("status", "==", status))
    
    query = query.limit(limit)
    docs = query.stream()
    
    reservations = []
    for doc in docs:
        reservations.append(doc.to_dict())
    
    # 作成日時の降順でソート
    reservations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return reservations

async def get_product_details(product_id: str) -> Optional[dict]:
    """商品詳細情報を取得"""
    db = get_firestore_db()
    product_doc = db.collection("products").document(product_id).get()
    
    if product_doc.exists:
        return product_doc.to_dict()
    return None

async def get_reservation_with_products(reservation_id: Optional[str] = None, reservation_number: Optional[str] = None) -> Optional[dict]:
    """予約詳細を取得（商品情報を含む）"""
    # 予約情報を取得
    if reservation_id:
        reservation = await get_reservation(reservation_id)
    elif reservation_number:
        reservation = await get_reservation_by_number(reservation_number)
    else:
        return None
    
    if not reservation:
        return None
    
    # 商品情報を取得して追加
    products = reservation.get("products", [])
    product_details = []
    
    for product_item in products:
        product_id = product_item.get("product_id")
        if product_id:
            product_info = await get_product_details(product_id)
            if product_info:
                product_details.append({
                    "product_id": product_id,
                    "name": product_info.get("name", ""),
                    "description": product_info.get("description", ""),
                    "price": product_info.get("price", 0),
                    "quantity": product_item.get("quantity", 0),
                })
            else:
                # 商品情報が取得できない場合は基本情報のみ
                product_details.append({
                    "product_id": product_id,
                    "name": "商品情報が見つかりません",
                    "description": "",
                    "price": 0,
                    "quantity": product_item.get("quantity", 0),
                })
    
    # 予約情報に商品詳細を追加
    reservation["product_details"] = product_details
    return reservation

async def complete_reservation(reservation_id: str) -> Optional[dict]:
    """予約を完了状態に更新"""
    db = get_firestore_db()
    doc_ref = db.collection("reservations").document(reservation_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None
    
    reservation_data = doc.to_dict()
    
    # 既に完了済みの場合はエラー
    if reservation_data.get("status") == "completed":
        raise ValueError("この予約は既に完了済みです")
    
    # キャンセル済みの予約は完了不可
    if reservation_data.get("status") == "cancelled":
        raise ValueError("キャンセル済みの予約は完了できません")
    
    # ステータスを完了に更新
    doc_ref.update({
        "status": "completed",
        "updated_at": datetime.now().isoformat(),
    })
    
    return doc_ref.get().to_dict()
