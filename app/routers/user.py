from typing import List
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, utils, oauth2
from app.database import get_db
from app.schemas import user as schema

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get(
    '/me',
    response_model=schema.UserOut
)
def get_current_user(
    current_user: int = Depends(oauth2.get_current_user)
):
    return current_user


@ router.get('/all', response_model=List[schema.UserOut])
def get_users(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # utils.check_for_root()
    results = db.query(models.User).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schema.UserOut
)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """
    Inserting a new user into the database
    """
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db_user = db.query(models.User).filter(
        models.User.email == new_user.email).first()

    if db_user:
        utils.unauthorized("Failed to create the User Already Exists !!!")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/info/{id}', response_model=schema.User)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    utils.check_for_root(current_user.role_id, 1)

    user = db.query(models.User).filter(models.User.user_id == id).first()
    if not user:
        utils.not_found(f"User with id: {id} does not exist!")

    return user
