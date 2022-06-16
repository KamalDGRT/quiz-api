from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserSimple
from app.schemas.topic import TopicCreate


class TopicPlayedCreate(BaseModel):
    topic_id: int
    topic_score: int

    class Config:
        orm_mode = True


class TopicPlayed(TopicPlayedCreate):
    topic_played_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TopicPlayedSimple(BaseModel):
    topic: TopicCreate
    player: UserSimple

    class Config:
        orm_mode = True


class TopicPlayedByMe(BaseModel):
    topic: TopicCreate
    topic_score: int

    class Config:
        orm_mode = True


class TopicPlayedComplete(TopicPlayed, TopicPlayedSimple):

    class Config:
        orm_mode = True
