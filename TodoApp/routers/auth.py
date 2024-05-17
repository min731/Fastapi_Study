from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter,Depends, HTTPException,status
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext # 암호화, 해싱
from sqlalchemy.orm import Session

# OAuth2PasswordRequestForm : Password Request Form ==> username, password 요구
# OAuth2PasswordBearer : 모든 API에서 토큰 확인
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
# JWT
from jose import jwt,JWTError

router = APIRouter(
    prefix='/auth', # 상위 url
    tags=['auth'] # Swagger UI tag 나누기
)
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# JWT
SECRET_KEY = 'ebe8a2b43cba148c2e93684bc14969e117b1b1e8c549fda1d87d02dad769787b' # 임의로 생성, openssl rand -hex 32
ALGORITHM = 'HS256'

# Bearer
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token') #  prefix 바뀌면 tokenURL도 수정

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

# JWT token,type 
class Token(BaseModel):
    access_token : str
    token_type : str


def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username : str, password : str, db):
    user = db.query(Users).filter(Users.username == username).first()
    
    # 유저 확인
    if not user:
        return False
    
    # 암호 확인
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    # 모두 맞다면 True
    return user

# JWT token 생성
# 관리자를 위해 role 추가
def create_access_token(username : str, user_id : int, role : str, expires_delta : timedelta):

    encode = {'sub':username, 'id':user_id, 'role':role}
    # token은 기간이 지나면 만료
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# 사용자의 token 확인
async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        #JWT Payload 확인
        # SECRET KEY, algorithm을 알아야함
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str  = payload.get('sub')
        user_id : str = payload.get('id')
        user_role : str = payload.get('role')

        if username is None or user_id is None:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        
        return {'username' : username , 'id' : user_id, 'user_role' : user_role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not valudate yser')


# @router.get("/auth/")
# async def get_user():
#     return {'user':'authenticated'}

@router.post("/",status_code=status.HTTP_201_CREATED)
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
        is_active = True,
        role = create_user_request.role
    )

    db.add(create_user_model)
    db.commit()

#JWT : JSON WEB TOKEN
# Header + Payload + Signature
# aaaaa.bbbbb.cccc

# Header : HS 256 algorithim + token type , Base64 encoding
# Payload : Claims(Registered, Public, Private), Base64 encoding
# Signature : Base64 encoding Header/Payload
# ==> JSON WEB TOKEN
# 한글자라도 바뀌면 'Invalid Signature'

@router.post("/token",response_model=Token)
# @router.post("/token")
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db : db_dependency):
    # OAyth2PasswordRequest : username , password 필요
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
    # return Token(**{'access_token': token, 'token_type': 'bearer'})