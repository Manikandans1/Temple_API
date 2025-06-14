# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from passlib.context import CryptContext
# from fastapi import Depends, HTTPException, status
# import os
# from dotenv import load_dotenv
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.models.user import User


# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.services.auth import OAuth
# from fastapi.responses import RedirectResponse
# from app.db.database import get_db
# from app.models.user import User
# from app.schemas.user import UserCreate, Token
# from app.services.auth import create_access_token

# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_user(token: str, db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # user_id: str = payload.get("sub")
#         # if user_id is None:
#         #     raise HTTPException(status_code=401, detail="Invalid token")

#         user_email = payload.get("sub")  # Assuming 'sub' contains the email

#         if not user_email:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


#         # user = db.query(User).filter(User.id == user_id).first()
#         user = db.query(User).filter(User.email == user_email).first()
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")

#         return user

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
    




# router = APIRouter()

# # OAuth Setup
# oauth = OAuth()

# oauth.register(
#     name='google',
#     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
#     authorize_url="https://accounts.google.com/o/oauth2/auth",
#     authorize_params={"scope": "openid email profile"},
#     access_token_url="https://oauth2.googleapis.com/token",
#     client_kwargs={"scope": "openid email profile"},
# )

# oauth.register(
#     name='facebook',
#     client_id=os.getenv("FACEBOOK_CLIENT_ID"),
#     client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
#     authorize_url="https://www.facebook.com/v14.0/dialog/oauth",
#     access_token_url="https://graph.facebook.com/v14.0/oauth/access_token",
#     client_kwargs={"scope": "email"},
# )

# oauth.register(
#     name='instagram',
#     client_id=os.getenv("INSTAGRAM_CLIENT_ID"),
#     client_secret=os.getenv("INSTAGRAM_CLIENT_SECRET"),
#     authorize_url="https://api.instagram.com/oauth/authorize",
#     access_token_url="https://api.instagram.com/oauth/access_token",
#     client_kwargs={"scope": "user_profile,user_media"},
# )