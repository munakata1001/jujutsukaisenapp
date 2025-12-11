# 商品関連のPydanticスキーマ
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 商品作成リクエスト
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(gt=0)
    order_start_date: datetime
    order_end_date: datetime
    max_per_reservation: int = Field(gt=0, default=10)
    max_per_user: int = Field(gt=0, default=5)
    total_order_limit: Optional[int] = Field(None, gt=0)
    is_active: bool = True

# 商品更新リクエスト
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    order_start_date: Optional[datetime] = None
    order_end_date: Optional[datetime] = None
    max_per_reservation: Optional[int] = Field(None, gt=0)
    max_per_user: Optional[int] = Field(None, gt=0)
    total_order_limit: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None

# 商品レスポンス
class ProductResponse(BaseModel):
    product_id: str
    name: str
    description: Optional[str]
    price: float
    order_start_date: datetime
    order_end_date: datetime
    max_per_reservation: int
    max_per_user: int
    total_order_limit: Optional[int]
    current_order_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 購入可能数確認レスポンス
class ProductAvailabilityResponse(BaseModel):
    available: bool
    available_count: int
    max_per_reservation: int
    max_per_user: int
    current_order_count: int
    total_order_limit: Optional[int]

