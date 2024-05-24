from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from ..database import Base
from sqlalchemy.orm import sessionmaker
from fastapi import status

# utils.py 파일에 모든 객체를 선언하고 불러옴
from .utils import *
from ..routers import todos

def test_read_all_authenticated(test_todo):
    response = client.get("/") # main.py에서 "/" 경로 시의 return 확인
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == [] # testdb.db에 아무것도 없을 시, True
    assert response.json() == [
        {   
            'id' : 1, # id는 자동 생성
            'title' : 'Learn to code',
            'description' : 'Need to learn everyday!',
            'priority' : 5,
            'complete' : False,
            'owner_id' : 1
            }
        ] # @pytest.fixture()로 객체 추가 후, True
    
def test_read_one_authenticated(test_todo): # 특정 todo_id 값 확인
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { # id == 1 값 한개 체크
                                'id' : 1, # id는 자동 생성
                                'title' : 'Learn to code',
                                'description' : 'Need to learn everyday!',
                                'priority' : 5,
                                'complete' : False,
                                'owner_id' : 1
                            } # @pytest.fixture()로 객체 추가 후, True
    
def test_read_one_authenticated_not_found(test_todo): # 특정 id의 값이 없을 때 확인 
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo not found.'}

def test_create_todo(test_todo): # 새 todo값 생성 확인, [test_todo 기입]
    request_data = {
        'title' : 'New Todo!',
        'description' : 'New Todo Description',
        'priority' : 5,
        'complete' : False,
        'owner_id' : 1
    }

    response = client.post("/todo/",json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')



def test_update_todo(test_todo): # 수정 확인
    request_data = {
        'title' : 'Change Todo!',
        'description' : 'Change Todo Description',
        'priority' : 5,
        'complete' : False,
        'owner_id' : 1
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_not_found(test_todo): # 수정 확인
    request_data = {
        'title' : 'Change Todo!',
        'description' : 'Change Todo Description',
        'priority' : 5,
        'complete' : False,
        'owner_id' : 1
    }

    response = client.put("/todo/999", json=request_data) # id 999 일때는 404
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Todo not found'}

def test_delete_todo(test_todo): # 삭제 확인
    response = client.delete("/todo/1")
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None # 삭제 했으므로 없음

def test_delete_todo(test_todo): # 삭제 확인
    response = client.delete("/todo/999") # 없는 id 이므로 404
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Todo not found.'}
    # print(response)