from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from ..models import Todos, Users
from ..database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(
    prefix='/user',
    tags=['user']
)
# uvicorn main:app --reload
# todos.db 와 pycache 생성

# JWT 발급 후 인증
from .auth import get_current_user
from passlib.context import CryptContext

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# Swagger UI 자물쇠 클릭후, username/password 입력
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):

    password : str
    new_password : str = Field(max_length=6)


@router.get("/",status_code=status.HTTP_200_OK)
async def get_user(user : user_dependency,
                   db : db_dependency):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user : user_dependency,
                          db : db_dependency,
                          user_verification : UserVerification):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()