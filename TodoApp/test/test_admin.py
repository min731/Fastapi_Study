from .utils import * # utils.py에 정리된 모든 객체 가져오기
from ..routers.admin import get_db, get_current_user # 원본 get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = overrride_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title' : 'Learn to code',
                                'description' : 'Need to learn everyday!',
                                'priority' : 5,
                                'complete' : False,
                                'owner_id' : 1,
                                'id' : 1}]
    
def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Todo not found'}