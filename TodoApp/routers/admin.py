from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(
    prefix='/admin', # 상위 url
    tags=['admin'] # Swagger UI tag 나누기
)
# uvicorn main:app --reload
# todos.db 와 pycache 생성

# JWT 발급 후 인증
from .auth import get_current_user


def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Swagger UI 자물쇠 클릭후, username/password 입력
user_dependency = Annotated[dict, Depends(get_current_user)]



@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(user : user_dependency,
                   db : db_dependency,
                   ):
    
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency,
                      db : db_dependency,
                      todo_id : int = Path(gt=0)):
    
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Todo not found')

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
 
    