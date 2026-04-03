from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SubTripDaySchedule as ScheduleModel
from app import schemas

router = APIRouter(prefix="/sub_trip_day_schedule", tags=["SubTripDaySchedule"])

@router.post("/", response_model=schemas.SubTripDaySchedule)
def create_day_schedule(item: schemas.SubTripDayScheduleCreate, db: Session = Depends(get_db)):
    obj = ScheduleModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.SubTripDaySchedule])
def list_day_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ScheduleModel).offset(skip).limit(limit).all()

@router.get("/{day_schedule_id}", response_model=schemas.SubTripDaySchedule)
def get_day_schedule(day_schedule_id: int, db: Session = Depends(get_db)):
    obj = db.query(ScheduleModel).filter(ScheduleModel.id == day_schedule_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return obj

@router.put("/{day_schedule_id}", response_model=schemas.SubTripDaySchedule)
def update_day_schedule(day_schedule_id: int, item: schemas.SubTripDayScheduleUpdate, db: Session = Depends(get_db)):
    obj = db.query(ScheduleModel).filter(ScheduleModel.id == day_schedule_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Schedule not found")
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{day_schedule_id}")
def delete_day_schedule(day_schedule_id: int, db: Session = Depends(get_db)):
    obj = db.query(ScheduleModel).filter(ScheduleModel.id == day_schedule_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}