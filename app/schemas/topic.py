from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserSimple


class TopicCreate(BaseModel):
    topic_name: str

    class Config:
        orm_mode = True


class Topic(TopicCreate):
    topic_id: int

    class Config:
        orm_mode = True


class TopicUpdate(Topic):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TopicComplete(TopicUpdate):
    creator: UserSimple
    updater: UserSimple

    class Config:
        orm_mode = True
