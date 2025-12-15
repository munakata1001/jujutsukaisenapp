# 予約枠関連のPydanticスキーマ
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# 予約枠作成リクエスト
class TimeSlotCreate(BaseModel):
    date: date
    time: str = Field(pattern=r"^\d{2}:\d{2}$", description="時間形式: HH:MM")
    capacity: int = Field(gt=0, description="定員数")

# 予約枠更新リクエスト
class TimeSlotUpdate(BaseModel):
    capacity: Optional[int] = Field(None, gt=0)
    is_available: Optional[bool] = None

# 予約枠レスポンス
class TimeSlotResponse(BaseModel):
    slot_id: str
    date: date
    time: str
    capacity: int
    reserved_count: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 空き状況確認レスポンス
class AvailabilityResponse(BaseModel):
    available: bool
    available_count: int
    capacity: int
    reserved_count: int

