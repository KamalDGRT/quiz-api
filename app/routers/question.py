from datetime import datetime
from fastapi import status, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, oauth2
from app.schemas import question as schema
from app.utils import not_found, check_for_root

router = APIRouter(
    prefix='/question',
    tags=['Questions']
)


@router.get(
    '/all',
    response_model=List[schema.QuestionSimple]
)
def get_Questions(
    db: Session = Depends(get_db),
):
    results = db.query(models.Question).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schema.Question,
)
def create_question(
    question: schema.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    new_question = models.Question(
        created_by=current_user.user_id,
        updated_by=current_user.user_id,
        **question.dict(),
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question

@router.post(
    '/create/many',
    status_code=status.HTTP_201_CREATED,
    response_model=List[schema.QuestionSimple],
)
def create_many_questions(
    questions: List[schema.QuestionCreate],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    new_questions = list()

    for question in questions:
        new_question = models.Question(
            created_by=current_user.user_id,
            updated_by=current_user.user_id,
            **question.dict(),
        )
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        new_questions.append(new_question)

    return new_questions

@router.get(
    '/info/{id}',
    response_model=schema.QuestionComplete
)
def get_Question(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    question = db.query(models.Question).filter(
        models.Question.question_id == id
    ).first()

    if not question:
        not_found(f"Question with id: {id} not found!")

    return question


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_question(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    question_query = db.query(
        models.Question
    ).filter(
        models.Question.question_id == id
    )
    question = question_query.first()

    if question is None:
        not_found(f"Question with id: {id} not found!")

    question_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schema.QuestionUpdate
)
def update_Question(
    id: int,
    updated_question: schema.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    check_for_root(current_user.role_id, 1)

    question_query = db.query(
        models.Question
    ).filter(
        models.Question.question_id == id
    )

    question = question_query.first()

    if question is None:
        not_found(f"Question with id: {id} not found!")

    updated_question_record = updated_question.dict()
    updated_question_record["updated_by"] = current_user.user_id
    updated_question_record["updated_at"] = datetime.now().astimezone()

    question_query.update(
        updated_question_record,
        synchronize_session=False
    )
    db.commit()

    return question_query.first()
