from datetime import datetime
from fastapi import status, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, oauth2
from app.schemas import topic as schema
from app.utils import not_found, check_for_root

router = APIRouter(
    prefix='/topic',
    tags=['Topics']
)


@router.get(
    '/all',
    response_model=List[schema.Topic]
)
def get_Topics(
    db: Session = Depends(get_db),
):
    results = db.query(models.Topic).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schema.Topic,
)
def create_topic(
    topic: schema.TopicCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    new_topic = models.Topic(
        created_by=current_user.user_id,
        updated_by=current_user.user_id,
        **topic.dict(),
    )

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic

@router.post(
    '/create/many',
    status_code=status.HTTP_201_CREATED,
    response_model=List[schema.Topic],
)
def create_many_topics(
    topics: List[schema.TopicCreate],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    new_topics = list()

    for topic in topics:
        new_topic = models.Topic(
            created_by=current_user.user_id,
            updated_by=current_user.user_id,
            **topic.dict(),
        )
        db.add(new_topic)
        db.commit()
        db.refresh(new_topic)
        new_topics.append(new_topic)

    return new_topics

@router.get(
    '/info/{id}',
    response_model=schema.TopicComplete
)
def get_Topic(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    topic = db.query(models.Topic).filter(
        models.Topic.topic_id == id
    ).first()

    if not topic:
        not_found(f"Topic with id: {id} not found!")

    return topic


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_topic(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    topic_query = db.query(
        models.Topic
    ).filter(
        models.Topic.topic_id == id
    )
    topic = topic_query.first()

    if topic is None:
        not_found(f"Topic with id: {id} not found!")

    topic_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schema.TopicUpdate
)
def update_Topic(
    id: int,
    updated_topic: schema.TopicCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    topic_query = db.query(
        models.Topic
    ).filter(
        models.Topic.topic_id == id
    )

    topic = topic_query.first()

    if topic is None:
        not_found(f"Topic with id: {id} not found!")

    updated_topic_record = updated_topic.dict()
    updated_topic_record["updated_by"] = current_user.user_id
    updated_topic_record["updated_at"] = datetime.now().astimezone()

    topic_query.update(
        updated_topic_record,
        synchronize_session=False
    )
    db.commit()

    return topic_query.first()
