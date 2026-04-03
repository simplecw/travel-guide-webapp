from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Hotel
from app import schemas

router = APIRouter(prefix="/hotel", tags=["Hotel"])

@router.post("/", response_model=schemas.HotelResponse, status_code=status.HTTP_201_CREATED)
def create_hotel(item: schemas.HotelCreate, db: Session = Depends(get_db)):
    obj = Hotel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.HotelResponse])
def list_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Hotel).order_by(Hotel.sort_order.asc().nullslast()).offset(skip).limit(limit).all()

@router.get("/{hotel_id}", response_model=schemas.HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    obj = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return obj

@router.put("/{hotel_id}", response_model=schemas.HotelResponse)
def update_hotel(hotel_id: int, item: schemas.HotelUpdate, db: Session = Depends(get_db)):
    obj = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    obj = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(obj)
    db.commit()
    return None