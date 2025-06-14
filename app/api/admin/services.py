from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.service import Service
from app.models.temple import Temple
from app.schemas.service import ServiceSchema, ServiceCreate
from app.db.database import get_db

router = APIRouter()

# ✅ Create a Service for a Specific Temple
@router.post("/temples/{temple_id}/services", response_model=ServiceSchema)
def create_service(temple_id: int, service: ServiceCreate, db: Session = Depends(get_db)):
    temple = db.query(Temple).filter(Temple.id == temple_id).first()
    if not temple:
        raise HTTPException(status_code=404, detail="Temple not found")

    new_service = Service(
        name=service.name,
        description=service.description,
        price=service.price,
        live_video_url=service.live_video_url,
        recorded_video_url=service.recorded_video_url,
        temple_id=temple_id
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

# ✅ Get All Services of a Specific Temple
@router.get("/temples/{temple_id}/services", response_model=list[ServiceSchema])
def get_services_by_temple(temple_id: int, db: Session = Depends(get_db)):
    return db.query(Service).filter(Service.temple_id == temple_id).all()

# ✅ Update a Service by ID
@router.put("/services/{service_id}", response_model=ServiceSchema)
def update_service(service_id: int, service_update: ServiceCreate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.name = service_update.name
    service.description = service_update.description
    service.price = service_update.price
    service.live_video_url = service_update.live_video_url
    service.recorded_video_url = service_update.recorded_video_url

    db.commit()
    db.refresh(service)
    return service

# ✅ Delete a Service
@router.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}
