from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()
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

# 요청 형식 지정
class TodoRequest(BaseModel):
    # id는 이미 pk로 지정
    title : str = Field(min_length=3)
    description : str = Field(min_length=3,max_length=100)
    priority : int = Field(gt=0,lt=6)
    complete : bool 

    class Config:
        json_schema_extra = {
            'example' : {
               'title' : 'title_tmp',
               'description' : 'description_tmp',
               'priority' : 1,
               'complete' : True 
            }
        }
        
@router.get("/",status_code=status.HTTP_200_OK)
# async def read_all(db : db_dependency):
# jwt 인증해야 가능
# 인증이후 자신의 todos만 보게끔 설정
async def read_all(user : user_dependency, db : db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    
    # return db.query(Todos).all()
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
# jwt 인증 추가
# async def read_todo(db : db_dependency, todo_id : int = Path(gt=0)):
async def read_todo(user : user_dependency, db : db_dependency, todo_id : int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    
    # first() : record만 반환
    # 모든 id를 다 찾는게 아닌 unique한 id값으로 1개 찾음

    # 요청한 todo_id가 같으면서 사용자의 todo 인 것
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first() 
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail='Todo not found.')

@router.post("/todo/",status_code=status.HTTP_201_CREATED)
# async def create_todo(db : db_dependency, todo_request : TodoRequest):
# 사용자 jwt 인증 추가
async def create_todo(user : user_dependency, db : db_dependency, todo_request : TodoRequest):

    # 사용자 jwt 인증 추가
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authencation Failed ')
    
    # todo_model = Todos(**todo_request.model_dump())
    todo_model = Todos(**todo_request.model_dump(),
                       owner_id = user.get('id')) # 등록자 id 추가
    
    db.add(todo_model)
    db.commit() # transaction

@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db : db_dependency,
                      todo_request : TodoRequest,
                      todo_id : int = Path(gt=0),
                      #todo_request : TodoRequest # 매개변수보다 앞에 있어야함
                      ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db : db_dependency, todo_id : int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found.')
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()


