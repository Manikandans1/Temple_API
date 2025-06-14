from pydantic import BaseModel

class AdminCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class AdminLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
