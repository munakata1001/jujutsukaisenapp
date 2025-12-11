from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# APIルーターをインポート
from app.api import calendar, timeslots, reservations, products

load_dotenv()

app = FastAPI(
    title="呪術廻戦ポップアップショップ予約API",
    description="ポップアップショップ予約カレンダーAPI",
    version="1.0.0"
)

# CORS設定
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターを登録
app.include_router(calendar.router)
app.include_router(timeslots.router)
app.include_router(timeslots.admin_router)
app.include_router(reservations.router)
app.include_router(products.router)
app.include_router(products.admin_router)

@app.get("/")
def read_root():
    return {"message": "呪術廻戦ポップアップショップ予約API"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

