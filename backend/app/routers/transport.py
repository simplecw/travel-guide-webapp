from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Transport
from app.schemas import TransportCreate, TransportUpdate, TransportRead

router = APIRouter(prefix="/transport", tags=["Transport"])

@router.post("/", response_model=TransportRead)
def create_transport(item: TransportCreate, db: Session = Depends(get_db)):
    obj = Transport(**item.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[TransportRead])
def list_transports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Transport).offset(skip).limit(limit).all()

@router.get("/{transport_id}", response_model=TransportRead)
def get_transport(transport_id: int, db: Session = Depends(get_db)):
    obj = db.query(Transport).filter(Transport.id == transport_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Transport not found")
    return obj

@router.put("/{transport_id}", response_model=TransportRead)
def update_transport(transport_id: int, item: TransportUpdate, db: Session = Depends(get_db)):
    obj = db.query(Transport).filter(Transport.id == transport_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Transport not found")
    
    update_data = item.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{transport_id}", response_model=dict)
def delete_transport(transport_id: int, db: Session = Depends(get_db)):
    obj = db.query(Transport).filter(Transport.id == transport_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Transport not found")
    db.delete(obj)
    db.commit()
    return {"message": "Transport deleted successfully"}