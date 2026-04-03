from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# 导入 models
from app.models import Base

# 导入路由模块
from app.routers import (
    trip_plan, trip_overview, sub_trip, sub_trip_day_schedule,
    sub_trip_day_timeline, sub_trip_day_meal, sub_trip_day_transport,
    attraction, food_item, hotel, transport, budget_item,
    expense_item, reference_item, packing_item, packing_template_item,
    todo_item, travel_note, review_item, requirement_item, users
)

app = FastAPI(title="Travel Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 数据库配置：动态从环境变量读取 ---
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "yourpassword")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "travel_db")

# 构建 MySQL 连接字符串 
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 针对 MySQL 的优化配置：增加连接检查和回收 
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 自动创建表结构 
Base.metadata.create_all(bind=engine)

# --- 注册路由 ---
# 建议：如果 router.py 内部已定义 prefix，此处直接 include 即可
app.include_router(trip_plan.router)
app.include_router(trip_overview.router)
app.include_router(sub_trip.router)
app.include_router(sub_trip_day_schedule.router)
app.include_router(sub_trip_day_timeline.router)
app.include_router(sub_trip_day_meal.router)
app.include_router(sub_trip_day_transport.router)
app.include_router(attraction.router)
app.include_router(food_item.router)
app.include_router(hotel.router)
app.include_router(transport.router)
app.include_router(budget_item.router)
app.include_router(expense_item.router)
app.include_router(reference_item.router)
app.include_router(packing_item.router)
app.include_router(packing_template_item.router)
app.include_router(todo_item.router)
app.include_router(travel_note.router)
app.include_router(review_item.router)
app.include_router(requirement_item.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Travel Planner API is running on MySQL via Docker!"}