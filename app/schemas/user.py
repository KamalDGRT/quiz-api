from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.schemas.role import RoleCreate


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role_id: int = 4


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    user_id: int
    full_name: str
    created_at: datetime
    role: RoleCreate

    class Config:
        orm_mode = True


class User(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    role: RoleCreate

    class Config:
        orm_mode = True
