# 商品管理サービス
import uuid
from datetime import datetime, date
from typing import List, Optional, Dict
from google.cloud.firestore_v1 import FieldFilter
from app.utils.firebase import get_firestore_db

async def create_product(product_data: dict) -> dict:
    """商品を作成"""
    db = get_firestore_db()
    product_id = str(uuid.uuid4())
    
    # 商品データを作成
    product_doc = {
        "product_id": product_id,
        "name": product_data["name"],
        "description": product_data.get("description", ""),
        "price": product_data["price"],
        "image_url": product_data.get("image_url"),
        "order_start_date": product_data["order_start_date"].isoformat() if isinstance(product_data["order_start_date"], datetime) else product_data["order_start_date"],
        "order_end_date": product_data["order_end_date"].isoformat() if isinstance(product_data["order_end_date"], datetime) else product_data["order_end_date"],
        "max_per_reservation": product_data.get("max_per_reservation", 10),
        "max_per_user": product_data.get("max_per_user", 5),
        "total_order_limit": product_data.get("total_order_limit"),
        "current_order_count": 0,
        "is_active": product_data.get("is_active", True),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    
    # Firestoreに保存
    db.collection("products").document(product_id).set(product_doc)
    
    return product_doc

async def get_product(product_id: str) -> Optional[dict]:
    """商品を取得"""
    db = get_firestore_db()
    doc = db.collection("products").document(product_id).get()
    
    if doc.exists:
        return doc.to_dict()
    return None

async def get_all_products(include_inactive: bool = False) -> List[dict]:
    """商品一覧を取得"""
    db = get_firestore_db()
    query = db.collection("products")
    
    # アクティブな商品のみ取得する場合
    if not include_inactive:
        query = query.where(filter=FieldFilter("is_active", "==", True))
    
    docs = query.stream()
    
    products = []
    for doc in docs:
        products.append(doc.to_dict())
    
    # 作成日時の降順でソート
    products.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return products

async def update_product(product_id: str, update_data: dict) -> Optional[dict]:
    """商品を更新"""
    db = get_firestore_db()
    doc_ref = db.collection("products").document(product_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None
    
    # datetime オブジェクトは文字列に変換
    if "order_start_date" in update_data and isinstance(update_data["order_start_date"], datetime):
        update_data["order_start_date"] = update_data["order_start_date"].isoformat()
    if "order_end_date" in update_data and isinstance(update_data["order_end_date"], datetime):
        update_data["order_end_date"] = update_data["order_end_date"].isoformat()
    
    update_data["updated_at"] = datetime.now().isoformat()
    doc_ref.update(update_data)
    
    return doc_ref.get().to_dict()

async def delete_product(product_id: str) -> bool:
    """商品を削除（論理削除：is_activeをFalseにする）"""
    db = get_firestore_db()
    doc_ref = db.collection("products").document(product_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return False
    
    doc_ref.update({
        "is_active": False,
        "updated_at": datetime.now().isoformat(),
    })
    
    return True

async def increment_order_count(product_id: str, quantity: int) -> bool:
    """商品の受注数を増やす"""
    db = get_firestore_db()
    doc_ref = db.collection("products").document(product_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return False
    
    current_count = doc.to_dict().get("current_order_count", 0)
    doc_ref.update({
        "current_order_count": current_count + quantity,
        "updated_at": datetime.now().isoformat(),
    })
    
    return True

async def decrement_order_count(product_id: str, quantity: int) -> bool:
    """商品の受注数を減らす"""
    db = get_firestore_db()
    doc_ref = db.collection("products").document(product_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return False
    
    current_count = doc.to_dict().get("current_order_count", 0)
    new_count = max(0, current_count - quantity)
    doc_ref.update({
        "current_order_count": new_count,
        "updated_at": datetime.now().isoformat(),
    })
    
    return True

async def get_product_availability(product_id: str) -> Dict:
    """商品の購入可能数を取得"""
    product = await get_product(product_id)
    
    if not product:
        return {
            "available": False,
            "available_count": 0,
            "max_per_reservation": 0,
            "max_per_user": 0,
            "current_order_count": 0,
            "total_order_limit": None,
        }
    
    total_limit = product.get("total_order_limit")
    current_count = product.get("current_order_count", 0)
    
    # 総受注数の上限がある場合
    if total_limit:
        available_count = max(0, total_limit - current_count)
    else:
        # 上限がない場合は、1予約あたりの最大購入数を返す
        available_count = product.get("max_per_reservation", 0)
    
    # 受注期間のチェック
    today = date.today()
    order_start = product.get("order_start_date")
    order_end = product.get("order_end_date")
    
    is_in_period = True
    if order_start:
        start_date = date.fromisoformat(order_start) if isinstance(order_start, str) else order_start
        if today < start_date:
            is_in_period = False
    
    if order_end:
        end_date = date.fromisoformat(order_end) if isinstance(order_end, str) else order_end
        if today > end_date:
            is_in_period = False
    
    is_available = (
        product.get("is_active", False) and
        is_in_period and
        available_count > 0
    )
    
    return {
        "available": is_available,
        "available_count": available_count if is_in_period else 0,
        "max_per_reservation": product.get("max_per_reservation", 0),
        "max_per_user": product.get("max_per_user", 0),
        "current_order_count": current_count,
        "total_order_limit": total_limit,
    }

async def check_user_purchase_limit(product_id: str, user_email: str, requested_quantity: int) -> bool:
    """ユーザーの購入制限をチェック"""
    db = get_firestore_db()
    product = await get_product(product_id)
    
    if not product:
        return False
    
    max_per_user = product.get("max_per_user", 0)
    if max_per_user <= 0:
        # 制限がない場合はOK
        return True
    
    # ユーザーの既存購入数を集計
    query = db.collection("reservations").where(
        filter=FieldFilter("user_email", "==", user_email)
    ).where(
        filter=FieldFilter("status", "in", ["pending", "confirmed"])
    )
    
    total_purchased = 0
    for res_doc in query.stream():
        res_data = res_doc.to_dict()
        for p in res_data.get("products", []):
            if p.get("product_id") == product_id:
                total_purchased += p.get("quantity", 0)
    
    # リクエスト数量を含めた合計が制限以内かチェック
    return (total_purchased + requested_quantity) <= max_per_user


