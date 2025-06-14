# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.models.user import User
# from app.schemas.user import UserCreate, UserLogin, Token
# from app.services.auth import hash_password, verify_password, create_access_token

# router = APIRouter()

# @router.post("/signup", response_model=Token)
# async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = hash_password(user.password)
#     new_user = User(name=user.name, email=user.email, phone=user.phone, hashed_password=hashed_password)

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     access_token = create_access_token({"sub": new_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/login", response_model=Token)
# async def user_login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     access_token = create_access_token({"sub": db_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}








# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.models.user import User
# from app.schemas.user import UserCreate, UserLogin, Token
# from app.services.auth_service import hash_password, verify_password, create_access_token
# from app.services.oauth_config import oauth
# from fastapi import Request


# router = APIRouter()

# # ------------------ SIGNUP -------------------
# @router.post("/signup", response_model=Token)
# async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = hash_password(user.password)
#     new_user = User(name=user.name, email=user.email, phone=user.phone, hashed_password=hashed_password)

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     access_token = create_access_token({"sub": new_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ LOGIN -------------------
# @router.post("/login", response_model=Token)
# async def user_login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     access_token = create_access_token({"sub": db_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ GOOGLE LOGIN -------------------
# @router.get("/auth/google")
# async def google_login():
#     return await oauth.google.authorize_redirect("http://localhost:8000/auth/google/callback")

# @router.get("/auth/google/callback")
# async def google_callback(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = token.get("userinfo", {})

#     email = user_info.get("email")
#     name = user_info.get("name")

#     if not email:
#         raise HTTPException(status_code=400, detail="Google login failed. No email provided.")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         user = User(name=name, email=email, hashed_password="")
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ FACEBOOK LOGIN -------------------
# @router.get("/auth/facebook")
# async def facebook_login():
#     return await oauth.facebook.authorize_redirect("http://localhost:8000/auth/facebook/callback")

# @router.get("/auth/facebook/callback")
# async def facebook_callback(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.facebook.authorize_access_token(request)
#     user_info = await oauth.facebook.get("https://graph.facebook.com/me?fields=id,name,email", token=token)
#     user_data = user_info.json()

#     email = user_data.get("email")
#     name = user_data.get("name")

#     if not email:
#         raise HTTPException(status_code=400, detail="Facebook login failed. No email provided.")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         user = User(name=name, email=email, hashed_password="")
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ INSTAGRAM LOGIN -------------------
# @router.get("/auth/instagram")
# async def instagram_login():
#     return await oauth.instagram.authorize_redirect("http://localhost:8000/auth/instagram/callback")

# @router.get("/auth/instagram/callback")
# async def instagram_callback(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.instagram.authorize_access_token(request)
#     user_info = await oauth.instagram.get("https://graph.instagram.com/me?fields=id,username", token=token)
#     user_data = user_info.json()

#     username = user_data.get("username")

#     if not username:
#         raise HTTPException(status_code=400, detail="Instagram login failed. No username provided.")

#     user = db.query(User).filter(User.email == username).first()
#     if not user:
#         user = User(name=username, email=f"{username}@instagram.com", hashed_password="")
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}












# # FastAPI Authentication Backend
# from fastapi import APIRouter, Depends, HTTPException, Request
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.models.user import User
# from app.schemas.user import UserCreate, UserLogin, Token
# from app.services.auth_service import hash_password, verify_password, create_access_token
# from app.services.oauth_config import oauth

# router = APIRouter()

# # ------------------ SIGNUP -------------------
# @router.post("/signup", response_model=Token)
# async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     hashed_password = hash_password(user.password)
#     new_user = User(name=user.name, email=user.email, phone=user.phone, hashed_password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     access_token = create_access_token({"sub": new_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ LOGIN -------------------
# @router.post("/login", response_model=Token)
# async def user_login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     access_token = create_access_token({"sub": db_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ GOOGLE LOGIN -------------------
# @router.get("/auth/google")
# async def google_login():
#     return await oauth.google.authorize_redirect("http://localhost:8000/auth/google/callback")

# @router.get("/auth/google/callback")
# async def google_callback(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = token.get("userinfo", {})
#     email = user_info.get("email")
#     name = user_info.get("name")
    
#     if not email:
#         raise HTTPException(status_code=400, detail="Google login failed. No email provided.")
    
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         user = User(name=name, email=email, hashed_password="")
#         db.add(user)
#         db.commit()
#         db.refresh(user)
    
#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ FACEBOOK LOGIN -------------------
# @router.get("/auth/facebook")
# async def facebook_login():
#     return await oauth.facebook.authorize_redirect("http://localhost:8000/auth/facebook/callback")

# @router.get("/auth/facebook/callback")
# async def facebook_callback(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.facebook.authorize_access_token(request)
#     user_info = await oauth.facebook.get("https://graph.facebook.com/me?fields=id,name,email", token=token)
#     user_data = user_info.json()
#     email = user_data.get("email")
#     name = user_data.get("name")
    
#     if not email:
#         raise HTTPException(status_code=400, detail="Facebook login failed. No email provided.")
    
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         user = User(name=name, email=email, hashed_password="")
#         db.add(user)
#         db.commit()
#         db.refresh(user)
    
#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # ------------------ INSTAGRAM LOGIN -------------------
# @router.get("/auth/instagram")
# async def instagram_login():
#     return await oauth.instagram.authorize_redirect("http://localhost:8000/auth/instagram/callback")

# @router.get("/auth/instagram/callback")
# async def instagram_callback(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.instagram.authorize_access_token(request)
#     user_info = await oauth.instagram.get("https://graph.instagram.com/me?fields=id,username", token=token)
#     user_data = user_info.json()
#     username = user_data.get("username")
    
#     if not username:
#         raise HTTPException(status_code=400, detail="Instagram login failed. No username provided.")
    
#     user = db.query(User).filter(User.email == username).first()
#     if not user:
#         user = User(name=username, email=f"{username}@instagram.com", hashed_password="")
#         db.add(user)
#         db.commit()
#         db.refresh(user)
    
#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import Token
from app.services.auth_service import create_access_token
from app.services.oauth_config import oauth
from authlib.integrations.starlette_client import OAuth

app = FastAPI()

# Enable SessionMiddleware (Required for OAuth)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

router = APIRouter()

# ------------------ GOOGLE LOGIN -------------------
@router.get("/auth/google")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request, "http://192.168.137.1:8000/user/auth/google/callback"
    )

@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo", {})

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Google login failed")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, hashed_password="")
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": user.email})
    
    # Redirect to a success page
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------ FACEBOOK LOGIN -------------------
@router.get("/auth/facebook")
async def facebook_login(request: Request):
    return await oauth.facebook.authorize_redirect(
        request, "http://192.168.137.1:8000/user/auth/facebook/callback"
    )

@router.get("/auth/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.facebook.authorize_access_token(request)
    user_info = await oauth.facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email", token=token
    )
    user_data = user_info.json()

    email = user_data.get("email")
    name = user_data.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Facebook login failed")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, hashed_password="")
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------ INSTAGRAM LOGIN -------------------
@router.get("/auth/instagram")
async def instagram_login(request: Request):
    return await oauth.instagram.authorize_redirect(
        request, "http://192.168.137.1:8000/user/auth/instagram/callback"
    )

@router.get("/auth/instagram/callback")
async def instagram_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.instagram.authorize_access_token(request)
    user_info = await oauth.instagram.get(
        "https://graph.instagram.com/me?fields=id,username", token=token
    )
    user_data = user_info.json()

    username = user_data.get("username")

    if not username:
        raise HTTPException(status_code=400, detail="Instagram login failed")

    email = f"{username}@instagram.com"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=username, email=email, hashed_password="")
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(router)
