# test함에 있어 engine, TestingSessionLocal, override_get_db(), override_get_user()
# 등의 모듈화 하기 위함 utils.py


from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from ..database import Base
from sqlalchemy.orm import sessionmaker
from fastapi import status
from ..main import app
from ..routers.todos import get_db,get_current_user
import pytest
from ..models import Todos, Users
from fastapi.testclient import TestClient

from ..routers.users import bcrypt_context

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


app.dependency_overrides[get_db] = overrride_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


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

@pytest.fixture
def test_user():
    user = Users(
        username = 'codingwithroby',
        email = 'codingwithrobytest@email.com',
        first_name = 'Eric',
        last_name = 'Roby',
        hashed_password = bcrypt_context.hash("testpassword"),
        role = 'admin',
        # phone_number = "(111)-111-1111"
        )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

client = TestClient(app)
 