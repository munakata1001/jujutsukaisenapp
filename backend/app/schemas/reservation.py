# 予約関連のPydanticスキーマ
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

# 予約ステータス
class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

# 商品情報（予約内で使用）
class ProductItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0, description="購入数量")

# 予約作成リクエスト
class ReservationCreate(BaseModel):
    user_email: EmailStr
    user_name: str = Field(min_length=1, max_length=100)
    user_phone: str = Field(min_length=10, max_length=20)
    visit_date: date
    visit_time: str = Field(pattern=r"^\d{2}:\d{2}$", description="時間形式: HH:MM")
    products: List[ProductItem] = Field(default_factory=list)

# 予約更新リクエスト
class ReservationUpdate(BaseModel):
    visit_date: Optional[date] = None
    visit_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    products: Optional[List[ProductItem]] = None

# 商品詳細情報（予約確認用）
class ProductDetail(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

# 予約レスポンス
class ReservationResponse(BaseModel):
    reservation_id: str
    reservation_number: str
    user_email: str
    user_name: str
    user_phone: str
    visit_date: date
    visit_time: str
    status: ReservationStatus
    products: List[ProductItem]
    created_at: datetime
    updated_at: datetime
    product_details: Optional[List[ProductDetail]] = None

    class Config:
        from_attributes = True
