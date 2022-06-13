from fastapi import APIRouter,  Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import token as schema
from app import models, utils, oauth2
from app.database import get_db


router = APIRouter(tags=['Authentication'])


@router.post(
    '/login',
    response_model=schema.Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user:
        utils.unauthorized("Invalid Credentials !!!")

    # if the passwords do not match
    if not utils.verify(
        user_credentials.password,
        user.password
    ):
        utils.unauthorized("Invalid Credentials !!!")

    # Create a Token & return it
    access_token = oauth2.create_access_token(
        data={
            "user_id": user.user_id
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
