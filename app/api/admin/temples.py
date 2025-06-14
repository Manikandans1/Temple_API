from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.temple import Temple
from app.schemas.temple import TempleSchema, TempleCreate
from app.db.database import get_db

router = APIRouter()

# ✅ Create a Temple
@router.post("/temples", response_model=TempleSchema)
def create_temple(temple: TempleCreate, db: Session = Depends(get_db)):
    new_temple = Temple(**temple.dict())
    db.add(new_temple)
    db.commit()
    db.refresh(new_temple)
    return new_temple

# ✅ Get All Temples
@router.get("/temples", response_model=list[TempleSchema])
def get_temples(db: Session = Depends(get_db)):
    return db.query(Temple).all()

# ✅ Get a Temple by ID
@router.get("/temples/{temple_id}", response_model=TempleSchema)
def get_temple(temple_id: int, db: Session = Depends(get_db)):
    temple = db.query(Temple).filter(Temple.id == temple_id).first()
    if not temple:
        raise HTTPException(status_code=404, detail="Temple not found")
    return temple

# ✅ Update a Temple
@router.put("/temples/{temple_id}", response_model=TempleSchema)
def update_temple(temple_id: int, temple_update: TempleCreate, db: Session = Depends(get_db)):
    temple = db.query(Temple).filter(Temple.id == temple_id).first()
    if not temple:
        raise HTTPException(status_code=404, detail="Temple not found")

    for key, value in temple_update.dict().items():
        setattr(temple, key, value)

    db.commit()
    db.refresh(temple)
    return temple

# ✅ Delete a Temple
@router.delete("/temples/{temple_id}")
def delete_temple(temple_id: int, db: Session = Depends(get_db)):
    temple = db.query(Temple).filter(Temple.id == temple_id).first()
    if not temple:
        raise HTTPException(status_code=404, detail="Temple not found")

    db.delete(temple)
    db.commit()
    return {"message": "Temple deleted successfully"}

