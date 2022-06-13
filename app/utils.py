
# This file will hold a bunch of utility functions

from fastapi import status, HTTPException
from passlib.context import CryptContext
from os.path import splitext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """
    Returns bcrypt hashed string
    """
    return pwd_context.hash(password)

# We could have done the below thing in the auth.py but we would have to
# import the above stuff again. So, it is better to group related stuff.


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def unauthorized(message):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message
    )


def not_found(message):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )


def check_for_root(user_role, admin_role):
    if user_role != admin_role or user_role is None:
        unauthorized("Not Authorized to perform requested action!")


def invalid_file_type(message):
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=message
    )


def is_valid_image_file(file_name):
    if splitext(file_name)[-1] not in [".jpg", ".jpeg", ".png"]:
        invalid_file_type("Only Image File Types are allowed.")


def error_uploading_file():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="There was an error uploading the file"
    )

def unprocessable_entity(message):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )
