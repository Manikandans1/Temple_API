from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminLogin, Token
from app.services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model=Token)
async def admin_signup(admin: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(admin.password)
    new_admin = Admin(name=admin.name, email=admin.email, phone=admin.phone, hashed_password=hashed_password)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    access_token = create_access_token({"sub": new_admin.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def admin_login(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin or not verify_password(admin.password, db_admin.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_admin.email})
    return {"access_token": access_token, "token_type": "bearer"}
