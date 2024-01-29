import os
import secrets
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from dotenv import load_dotenv
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.db import crud
from src.db.database import get_db


load_dotenv()


security = HTTPBasic()
password_hasher = PasswordHasher()

API_ADMIN_USERNAME = os.getenv('API_ADMIN_USERNAME')
API_ADMIN_PASSWORD = os.getenv('API_ADMIN_PASSWORD')


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security),
                      db: Session = Depends(get_db)) -> UUID:
    username = credentials.username
    password = credentials.password

    user = crud.user_get_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    persisted_password = user.password

    try:
        password_hasher.verify(persisted_password, password)
    except Argon2Error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user.id


def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    username = credentials.username.encode('utf-8')
    password = credentials.password.encode('utf-8')

    is_correct_username = secrets.compare_digest(username, API_ADMIN_USERNAME.encode('utf-8'))
    is_correct_password = secrets.compare_digest(password, API_ADMIN_PASSWORD.encode('utf-8'))

    if not (is_correct_username and is_correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are unauthorized to perform admin actions.")
