from .utils import *
from ..routers.users import get_db # 개별 get_db , get_current_user는 동일
# from ..routers.users import get_db, get_current_user
# from ..routers.users import get_current_user

app.dependency_overrides[get_db] = overrride_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user): # test_user fixture 불러오기
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == None # test_user fixture가 없을 시에는 True
    # assert response.json() == {
    #                             'id' : 1,
    #                             'username' : 'codingwithroby',
    #                             'email' : 'codingwithrobytest@email.com',
    #                             'first_name' : 'Eric',
    #                             'last_name' : 'Roby',
    #                             'hashed_password' : bcrypt_context.hash("testpassword"),
    #                             'role' : 'admin',
    #                             # 'phone_number' : "(111)-111-1111",
    #                             'is_active' : True,
    #                             }
    assert response.json()['username'] == 'codingwithroby'
    assert response.json()['email'] == 'codingwithrobytest@email.com'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['role'] == 'admin'
    assert response.json()['is_active'] == True
    # assert response.json()['hashed_password'] == bcrypt_context.hash("testpassword")
    # 데이터를 hash()하면 매번 바뀌기 때문에, 바뀐 hash 데이터를 vertify하여 역으로 확인 
    assert bcrypt_context.verify("testpassword", response.json()['hashed_password'])

def test_change_password_success(test_user):
    response = client.put("/user/password",json={"password" : "testpassword",
                                                 "new_password" : "new123"})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalied_current_password(test_user):
    response = client.put("/user/password",json={"password" : "wrong_password",
                                                 "new_password" : "new123"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail' : 'Authentication Failed'}