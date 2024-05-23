from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from ..database import Base
from sqlalchemy.orm import sessionmaker
from fastapi import status

# test용 DB <-> Production DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread" : False},
    poolclass = StaticPool,
    )

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine) # testdb.db 생김






def overrride_get_db():

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'codingwithrobytest','id':1,'user_role':'admin'}

from ..main import app
from ..routers.todos import get_db,get_current_user

app.dependency_overrides[get_db] = overrride_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

import pytest
from ..models import Todos

@pytest.fixture # 객체 고정
def test_todo():
    todo = Todos(
        title = 'Learn to code',
        description = 'Need to learn everyday!',
        priority = 5,
        complete = False,
        owner_id = 1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo # test_read_all_authenticated()를 위해 yield
    with engine.connect() as connection: # 이후 매번 DB에서 삭제하여 초기화
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

from fastapi.testclient import TestClient
client = TestClient(app)


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

