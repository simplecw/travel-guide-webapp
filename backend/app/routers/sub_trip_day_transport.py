from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SubTripDayTransport
from app.schemas import DayTransportCreate, DayTransportUpdate, DayTransport

router = APIRouter(prefix="/sub_trip_day_transport", tags=["SubTripDayTransport"])

@router.post("/", response_model=DayTransport)
def create_day_transport(item: DayTransportCreate, db: Session = Depends(get_db)):
    obj = SubTripDayTransport(**item.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[DayTransport])
def list_day_transports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(SubTripDayTransport).offset(skip).limit(limit).all()

@router.get("/{transport_id}", response_model=DayTransport)
def get_day_transport(transport_id: int, db: Session = Depends(get_db)):
    obj = db.query(SubTripDayTransport).filter(SubTripDayTransport.id == transport_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="DayTransport not found")
    return obj

@router.put("/{transport_id}", response_model=DayTransport)
def update_day_transport(transport_id: int, item: DayTransportUpdate, db: Session = Depends(get_db)):
    obj = db.query(SubTripDayTransport).filter(SubTripDayTransport.id == transport_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="DayTransport not found")
    
    update_data = item.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{transport_id}", response_model=dict)
def delete_day_transport(transport_id: int, db: Session = Depends(get_db)):
    obj = db.query(SubTripDayTransport).filter(SubTripDayTransport.id == transport_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="DayTransport not found")
    db.delete(obj)
    db.commit()
    return {"message": "DayTransport deleted successfully"}