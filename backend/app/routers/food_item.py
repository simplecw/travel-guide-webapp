from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import FoodItem
from app import schemas

router = APIRouter(prefix="/food_item", tags=["FoodItem"])

# --- CREATE (增) ---
@router.post("/", response_model=schemas.FoodItemResponse, status_code=status.HTTP_201_CREATED)
def create_food(item: schemas.FoodItemCreate, db: Session = Depends(get_db)):
    """创建美食/餐厅记录"""
    obj = FoodItem(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# --- READ ALL (查列表) ---
@router.get("/", response_model=List[schemas.FoodItemResponse])
def list_foods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取美食列表，按 sort_order 排序"""
    return db.query(FoodItem).order_by(FoodItem.sort_order.asc()).offset(skip).limit(limit).all()

# --- READ ONE (查单个) ---
@router.get("/{food_id}", response_model=schemas.FoodItemResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    """根据ID获取详情"""
    obj = db.query(FoodItem).filter(FoodItem.id == food_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该记录")
    return obj

# --- UPDATE (改) ---
@router.put("/{food_id}", response_model=schemas.FoodItemResponse)
def update_food(food_id: int, item: schemas.FoodItemUpdate, db: Session = Depends(get_db)):
    """更新记录"""
    obj = db.query(FoodItem).filter(FoodItem.id == food_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该记录")
    
    # 仅更新传入的字段
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

# --- DELETE (删) ---
@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food(food_id: int, db: Session = Depends(get_db)):
    """删除记录"""
    obj = db.query(FoodItem).filter(FoodItem.id == food_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该记录")
    
    db.delete(obj)
    db.commit()
    return None