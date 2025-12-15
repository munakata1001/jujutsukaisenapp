# カレンダー関連のPydanticスキーマ
from pydantic import BaseModel
from typing import Dict

# カレンダーデータレスポンス
class CalendarDataResponse(BaseModel):
    year: int
    month: int
    data: Dict[int, dict]  # 日付をキー、予約状況を値とする辞書

