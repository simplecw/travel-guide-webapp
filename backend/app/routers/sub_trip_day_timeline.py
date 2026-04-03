from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SubTripDayTimeline
from app.schemas import TimelineCreate, TimelineUpdate, Timeline

router = APIRouter(prefix="/sub_trip_day_timeline", tags=["SubTripDayTimeline"])

@router.post("/", response_model=Timeline)
def create_timeline(item: TimelineCreate, db: Session = Depends(get_db)):
    obj = SubTripDayTimeline(**item.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[Timeline])
def list_timelines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(SubTripDayTimeline).offset(skip).limit(limit).all()

@router.get("/{timeline_id}", response_model=Timeline)
def get_timeline(timeline_id: int, db: Session = Depends(get_db)):
    obj = db.query(SubTripDayTimeline).filter(SubTripDayTimeline.id == timeline_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Timeline not found")
    return obj

@router.put("/{timeline_id}", response_model=Timeline)
def update_timeline(timeline_id: int, item: TimelineUpdate, db: Session = Depends(get_db)):
    obj = db.query(SubTripDayTimeline).filter(SubTripDayTimeline.id == timeline_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Timeline not found")
    
    update_data = item.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{timeline_id}", response_model=dict)
def delete_timeline(timeline_id: int, db: Session = Depends(get_db)):
    obj = db.query(SubTripDayTimeline).filter(SubTripDayTimeline.id == timeline_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Timeline not found")
    db.delete(obj)
    db.commit()
    return {"message": "Timeline deleted successfully"}