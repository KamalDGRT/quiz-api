from fastapi import status, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, oauth2
from app.schemas import topic_played as schema
from app.utils import not_found, check_for_root, unauthorized

router = APIRouter(
    prefix='/topic-played',
    tags=['Topics Played']
)


@router.get(
    '/all',
    response_model=List[schema.TopicPlayedSimple]
)
def get_Topics_Played(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)
    results = db.query(models.TopicPlayed).all()
    return results

@router.get(
    '/me',
    response_model=List[schema.TopicPlayedByMe]
)
def get_Topics_Played_by_Current_User(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    results = db.query(models.TopicPlayed).filter(
        models.TopicPlayed.played_by == current_user.user_id
    ).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schema.TopicPlayed,
)
def add_new_record_for_user(
    topic_played: schema.TopicPlayedCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    new_topic_played = models.TopicPlayed(
        played_by=current_user.user_id,
        **topic_played.dict(),
    )

    db.add(new_topic_played)
    db.commit()
    db.refresh(new_topic_played)

    return new_topic_played


@router.get(
    '/info/{id}',
    response_model=schema.TopicPlayedComplete
)
def get_Topic_Played_Info(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    topic_played = db.query(models.TopicPlayed).filter(
        models.TopicPlayed.topic_played_id == id
    ).first()

    if not topic_played:
        not_found(f"Topic Played with id: {id} not found!")

    return topic_played


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_topic_played(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    topic_played_query = db.query(
        models.TopicPlayed
    ).filter(
        models.TopicPlayed.topic_played_id == id
    )
    topic_played = topic_played_query.first()

    if topic_played is None:
        not_found(f"Topic Played with id: {id} not found!")

    if topic_played.played_by != current_user.user_id or current_user.role_id != 1:
        unauthorized("You are not authorized to do this.")

    topic_played_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
