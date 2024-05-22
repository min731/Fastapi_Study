# Client 테스트
from fastapi.testclient import TestClient
from fastapi import status


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..main import app
client = TestClient(app) 


# client가 GET 했는지 체크
def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK # HTTP 코드 확인
    assert response.json() == {'status' : 'Healthy'} # return 확인