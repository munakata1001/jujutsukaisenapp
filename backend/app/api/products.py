# 商品関連API
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductAvailabilityResponse
)
from app.services.product_service import (
    create_product as create_product_service,
    get_product as get_product_service,
    get_all_products,
    update_product as update_product_service,
    get_product_availability,
)

def _parse_datetime_str(dt_str: str) -> datetime:
    """ISO形式の文字列をdatetimeオブジェクトに変換"""
    if isinstance(dt_str, datetime):
        return dt_str
    try:
        # ISO形式の文字列を解析（タイムゾーン情報がある場合）
        if dt_str.endswith("Z"):
            dt_str = dt_str.replace("Z", "+00:00")
        return datetime.fromisoformat(dt_str)
    except (ValueError, AttributeError, TypeError):
        # フォールバック: より単純な形式を試す
        try:
            # ミリ秒を含む場合の処理
            if "." in dt_str and "+" not in dt_str and "Z" not in dt_str:
                # ミリ秒を除去
                dt_str = dt_str.split(".")[0]
            return datetime.fromisoformat(dt_str)
        except ValueError:
            # それでも失敗した場合は現在時刻を返す（エラー回避）
            return datetime.now()

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=List[ProductResponse])
async def get_products():
    """商品一覧を取得"""
    try:
        products = await get_all_products(include_inactive=False)
        # 日付文字列をdatetimeオブジェクトに変換
        for product in products:
            if product.get("order_start_date"):
                product["order_start_date"] = _parse_datetime_str(product["order_start_date"])
            if product.get("order_end_date"):
                product["order_end_date"] = _parse_datetime_str(product["order_end_date"])
            if product.get("created_at"):
                product["created_at"] = _parse_datetime_str(product["created_at"])
            if product.get("updated_at"):
                product["updated_at"] = _parse_datetime_str(product["updated_at"])
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"商品一覧の取得に失敗しました: {str(e)}")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_api(product_id: str):
    """商品詳細を取得"""
    try:
        product = await get_product_service(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="商品が見つかりません")
        
        # 日付文字列をdatetimeオブジェクトに変換
        if product.get("order_start_date"):
            product["order_start_date"] = _parse_datetime_str(product["order_start_date"])
        if product.get("order_end_date"):
            product["order_end_date"] = _parse_datetime_str(product["order_end_date"])
        if product.get("created_at"):
            product["created_at"] = _parse_datetime_str(product["created_at"])
        if product.get("updated_at"):
            product["updated_at"] = _parse_datetime_str(product["updated_at"])
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"商品の取得に失敗しました: {str(e)}")

@router.get("/{product_id}/availability", response_model=ProductAvailabilityResponse)
async def check_product_availability_api(product_id: str):
    """購入可能数確認"""
    try:
        product = await get_product_service(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="商品が見つかりません")
        
        availability = await get_product_availability(product_id)
        return availability
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"購入可能数の確認に失敗しました: {str(e)}")

# 管理者用API
admin_router = APIRouter(prefix="/api/admin/products", tags=["admin-products"])

@admin_router.post("", response_model=ProductResponse)
async def create_product_api(product: ProductCreate):
    """商品を登録（管理者）"""
    try:
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image_url": product.image_url,
            "order_start_date": product.order_start_date,
            "order_end_date": product.order_end_date,
            "max_per_reservation": product.max_per_reservation,
            "max_per_user": product.max_per_user,
            "total_order_limit": product.total_order_limit,
            "is_active": product.is_active,
        }
        result = await create_product_service(product_data)
        
        # 日付文字列をdatetimeオブジェクトに変換
        if result.get("order_start_date"):
            result["order_start_date"] = _parse_datetime_str(result["order_start_date"])
        if result.get("order_end_date"):
            result["order_end_date"] = _parse_datetime_str(result["order_end_date"])
        if result.get("created_at"):
            result["created_at"] = _parse_datetime_str(result["created_at"])
        if result.get("updated_at"):
            result["updated_at"] = _parse_datetime_str(result["updated_at"])
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"商品の登録に失敗しました: {str(e)}")

@admin_router.put("/{product_id}", response_model=ProductResponse)
async def update_product_api(product_id: str, product_update: ProductUpdate):
    """商品を更新（管理者）"""
    try:
        update_data = {}
        if product_update.name is not None:
            update_data["name"] = product_update.name
        if product_update.description is not None:
            update_data["description"] = product_update.description
        if product_update.price is not None:
            update_data["price"] = product_update.price
        if product_update.image_url is not None:
            update_data["image_url"] = product_update.image_url
        if product_update.order_start_date is not None:
            update_data["order_start_date"] = product_update.order_start_date
        if product_update.order_end_date is not None:
            update_data["order_end_date"] = product_update.order_end_date
        if product_update.max_per_reservation is not None:
            update_data["max_per_reservation"] = product_update.max_per_reservation
        if product_update.max_per_user is not None:
            update_data["max_per_user"] = product_update.max_per_user
        if product_update.total_order_limit is not None:
            update_data["total_order_limit"] = product_update.total_order_limit
        if product_update.is_active is not None:
            update_data["is_active"] = product_update.is_active
        
        result = await update_product_service(product_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail="商品が見つかりません")
        
        # 日付文字列をdatetimeオブジェクトに変換
        if result.get("order_start_date"):
            result["order_start_date"] = _parse_datetime_str(result["order_start_date"])
        if result.get("order_end_date"):
            result["order_end_date"] = _parse_datetime_str(result["order_end_date"])
        if result.get("created_at"):
            result["created_at"] = _parse_datetime_str(result["created_at"])
        if result.get("updated_at"):
            result["updated_at"] = _parse_datetime_str(result["updated_at"])
        
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"商品の更新に失敗しました: {str(e)}")



