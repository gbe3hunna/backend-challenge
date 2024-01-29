import logging

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.v1.auth import password_hasher, authenticate_admin
from src.db.crud import user_create
from src.db.database import get_db_fastapi
from src.schemas import ECGUser, ECGUserCreate, BaseResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/admin',
                   tags=['admin'])


@router.post('/register_user', status_code=status.HTTP_201_CREATED, response_model=BaseResponse)
async def register_user(user: ECGUser,
                        db: Session = Depends(get_db_fastapi),
                        _=Depends(authenticate_admin)):
    extended_user = ECGUserCreate(**user.model_dump(),
                                  hashed_password=password_hasher.hash(user.password))

    created_user = user_create(extended_user, db=db)
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Client {user.username} already exists.')

    return BaseResponse(message=f'User {user.username} with ID {user.id} was successfully created')
