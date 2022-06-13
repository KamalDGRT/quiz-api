"""
    We use pydantic models that does the part of data
    validation.
    It is because of this we can ensure that whatever
    data is sent by the frontend is in compliance
    with the backend.
"""

from datetime import datetime
from pydantic import BaseModel


class RoleCreate(BaseModel):
    role_name: str

    class Config:
        orm_mode = True

class Role(RoleCreate):
    role_id: int
    created_at: datetime

    class Config:
        orm_mode = True
