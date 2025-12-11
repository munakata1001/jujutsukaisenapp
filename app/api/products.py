# 商品関連API
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductAvailabilityResponse
)

router = APIRouter(prefix="/api/products", tags=["products"])

# 簡易実装（Firestore実装は今後拡張）
@router.get("", response_model=List[ProductResponse])
async def get_products():
    """商品一覧を取得"""
    # デモ用のダミーデータ
    return []

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """商品詳細を取得"""
    raise HTTPException(status_code=404, detail="商品が見つかりません")

@router.get("/{product_id}/availability", response_model=ProductAvailabilityResponse)
async def check_product_availability(product_id: str):
    """購入可能数確認"""
    raise HTTPException(status_code=404, detail="商品が見つかりません")

# 管理者用API
admin_router = APIRouter(prefix="/api/admin/products", tags=["admin-products"])

@admin_router.post("", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """商品を登録（管理者）"""
    raise HTTPException(status_code=501, detail="商品登録機能は今後実装予定です")

@admin_router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate):
    """商品を更新（管理者）"""
    raise HTTPException(status_code=501, detail="商品更新機能は今後実装予定です")

