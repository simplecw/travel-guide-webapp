from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import TripPlan as TripPlanModel
from app import schemas

router = APIRouter(prefix="/trip_plan", tags=["TripPlan"])

@router.post("/", response_model=schemas.TripPlan)
def create_trip_plan(item: schemas.TripPlanCreate, db: Session = Depends(get_db)):
    obj = TripPlanModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.TripPlan])
def list_trip_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TripPlanModel).offset(skip).limit(limit).all()

@router.get("/{trip_id}", response_model=schemas.TripPlan)
def get_trip_plan(trip_id: int, db: Session = Depends(get_db)):
    obj = db.query(TripPlanModel).filter(TripPlanModel.id == trip_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TripPlan not found")
    return obj

@router.put("/{trip_id}", response_model=schemas.TripPlan)
def update_trip_plan(trip_id: int, item: schemas.TripPlanUpdate, db: Session = Depends(get_db)):
    obj = db.query(TripPlanModel).filter(TripPlanModel.id == trip_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TripPlan not found")
    
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{trip_id}", response_model=dict)
def delete_trip_plan(trip_id: int, db: Session = Depends(get_db)):
    obj = db.query(TripPlanModel).filter(TripPlanModel.id == trip_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TripPlan not found")
    db.delete(obj)
    db.commit()
    return {"detail": "deleted"}