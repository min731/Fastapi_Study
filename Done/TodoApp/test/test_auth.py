from .utils import *
from ..routers.auth import get_db

# 함수를 직접 import해서 테스트
from ..routers.auth import authenticate_user

app.dependency_overrides[get_db] = overrride_get_db

def test_authenticated_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username,
                                           'testpassword',
                                           db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('WrongUserName',
                                          'testpassword',
                                          db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username,
                                            'wrongpaassword',
                                            db)
    assert wrong_password_user is False



from ..routers.auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username,
                                user_id,
                                role,
                                expires_delta)
    decoded_token =jwt.decode(token,
                              SECRET_KEY,
                              ALGORITHM,
                              options={'vertify_signature':False})
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

from ..routers.auth import get_current_user
import pytest
# async 함수인 get_current_user 테스트
@pytest.mark.asyncio #==> pytest-asyncio 라이브리로 async함수 테스트 가능
async def test_get_current_user_valid_token():

    encode = {'sub':'testuser',
              'id':1,
              'role':'admin'}
    token = jwt.encode(encode,
                       SECRET_KEY,
                       algorithm=ALGORITHM)
    
    # async함수이기 때문에 awit로 호출
    user = await get_current_user(token=token)
    assert user == {'username':'testuser',
                    'id':1,
                    'user_role':'admin'}
    
    ### pytest는 async 함수를 test할 수 없어 ==> skipped
    ### 대신 pytest-asyncio를 활용하면 됌 



from fastapi import HTTPException

@pytest.mark.asyncio
async def test_get_current_user_missing_payload(): # payload 만료 테스트
    encode = {'rolde':'user'}
    token = jwt.encode(encode,
                       SECRET_KEY,
                       algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Cound not valudate user.'
