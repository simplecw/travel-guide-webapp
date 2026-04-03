from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Attraction
from app import schemas

router = APIRouter(prefix="/attraction", tags=["Attraction"])

# --- CREATE (增) ---
@router.post("/", response_model=schemas.AttractionResponse, status_code=status.HTTP_201_CREATED)
def create_attraction(item: schemas.AttractionCreate, db: Session = Depends(get_db)):
    # 使用 model_dump() 确保数据类型正确转换
    obj = Attraction(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# --- READ ALL (查列表) ---
@router.get("/", response_model=List[schemas.AttractionResponse])
def list_attractions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Attraction).offset(skip).limit(limit).all()

# --- READ ONE (查单个) ---
@router.get("/{attraction_id}", response_model=schemas.AttractionResponse)
def get_attraction(attraction_id: int, db: Session = Depends(get_db)):
    obj = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该景点记录")
    return obj

# --- UPDATE (改) ---
@router.put("/{attraction_id}", response_model=schemas.AttractionResponse)
def update_attraction(attraction_id: int, item: schemas.AttractionUpdate, db: Session = Depends(get_db)):
    obj = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该景点记录")
    
    # 排除未设置的字段，实现局部更新
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

# --- DELETE (删) ---
@router.delete("/{attraction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attraction(attraction_id: int, db: Session = Depends(get_db)):
    obj = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该景点记录")
    
    db.delete(obj)
    db.commit()
    return None