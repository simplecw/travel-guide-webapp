from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SubTrip as SubTripModel
from app import schemas

router = APIRouter(prefix="/sub_trip", tags=["SubTrip"])

@router.post("/", response_model=schemas.SubTrip)
def create_sub_trip(item: schemas.SubTripCreate, db: Session = Depends(get_db)):
    obj = SubTripModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.SubTrip])
def list_sub_trips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(SubTripModel).order_by(SubTripModel.sort_order).offset(skip).limit(limit).all()

@router.get("/{sub_trip_id}", response_model=schemas.SubTrip)
def get_sub_trip(sub_trip_id: int, db: Session = Depends(get_db)):
    obj = db.query(SubTripModel).filter(SubTripModel.id == sub_trip_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="SubTrip not found")
    return obj

@router.put("/{sub_trip_id}", response_model=schemas.SubTrip)
def update_sub_trip(sub_trip_id: int, item: schemas.SubTripUpdate, db: Session = Depends(get_db)):
    obj = db.query(SubTripModel).filter(SubTripModel.id == sub_trip_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="SubTrip not found")
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{sub_trip_id}")
def delete_sub_trip(sub_trip_id: int, db: Session = Depends(get_db)):
    obj = db.query(SubTripModel).filter(SubTripModel.id == sub_trip_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="SubTrip not found")
    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}