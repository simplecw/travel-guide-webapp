from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional 
from app.database import get_db
from app.models import PackingItem
from app import schemas

router = APIRouter(prefix="/packing_item", tags=["PackingItem"])

@router.post("/", response_model=schemas.PackingItemResponse, status_code=status.HTTP_201_CREATED)
def create_packing(item: schemas.PackingItemCreate, db: Session = Depends(get_db)):
    obj = PackingItem(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.PackingItemResponse])
def list_packing(trip_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(PackingItem)
    if trip_id:
        query = query.filter(PackingItem.trip_id == trip_id)
    return query.all()

@router.get("/{packing_id}", response_model=schemas.PackingItemResponse)
def get_packing(packing_id: int, db: Session = Depends(get_db)):
    obj = db.query(PackingItem).filter(PackingItem.id == packing_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="PackingItem not found")
    return obj

@router.put("/{packing_id}", response_model=schemas.PackingItemResponse)
def update_packing(packing_id: int, item: schemas.PackingItemUpdate, db: Session = Depends(get_db)):
    obj = db.query(PackingItem).filter(PackingItem.id == packing_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="PackingItem not found")
    
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{packing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_packing(packing_id: int, db: Session = Depends(get_db)):
    obj = db.query(PackingItem).filter(PackingItem.id == packing_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="PackingItem not found")
    db.delete(obj)
    db.commit()
    return None