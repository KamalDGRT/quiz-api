from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import UserSimple
from app.schemas.topic import TopicCreate

class QuestionCreate(BaseModel):
    topic_id:int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str

    class Config:
        orm_mode = True


class Question(QuestionCreate):
    question_id: int

    class Config:
        orm_mode = True


class QuestionUpdate(Question):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class QuestionComplete(QuestionUpdate):
    topic: TopicCreate
    creator: UserSimple
    updater: UserSimple

    class Config:
        orm_mode = True

class QuestionSimple(BaseModel):
    question_id: int
    question_text: str
    topic: TopicCreate
    
    class Config:
        orm_mode = True
