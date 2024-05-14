from typing import Annotated
from fastapi import APIRouter,Depends,status
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext # 암호화, 해싱
from sqlalchemy.orm import Session

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str

    class Config:
        json_schema_extra = {
            'example' : {
               'username' : 'codingwithroby',
               'email' : 'codingwithroby@email.com',
               'first_name' : 'Eric',
               'last_name' : 'roby',
               'password' : '1234',
                'role' : 'admin'
            }
        }


def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/auth/")
async def get_user():
    return {'user':'authenticated'}

@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency,
                      create_user_request : CreateUserRequest):
    # password를 요청했지만 Users는 hashed_password가 필요하기 때문에 오류
    # create_user_model = Users(**create_user_request.model_dump())
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        # password는 hash
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()